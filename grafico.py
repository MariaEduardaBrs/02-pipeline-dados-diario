"""Gera um gráfico de linhas em SVG com a temperatura de cada cidade."""
from html import escape
from pathlib import Path

LARGURA = 720
ALTURA = 360
MARGEM = 50
CORES = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]


def agrupar_por_cidade(linhas):
    """Transforma linhas do CSV em {cidade: [temperaturas em ordem de tempo]}."""
    series = {}
    for linha in sorted(linhas, key=lambda item: item["momento"]):
        series.setdefault(linha["cidade"], []).append(float(linha["temperatura_c"]))
    return series


def gerar_svg(series):
    if not series:
        raise ValueError("Não há dados para desenhar.")

    todos = [valor for valores in series.values() for valor in valores]
    minimo, maximo = min(todos), max(todos)
    faixa = (maximo - minimo) or 1.0
    total_pontos = max(len(valores) for valores in series.values())
    largura_util = LARGURA - 2 * MARGEM
    altura_util = ALTURA - 2 * MARGEM
    base = ALTURA - MARGEM

    def posicao_x(indice):
        if total_pontos == 1:
            return MARGEM + largura_util / 2
        return MARGEM + largura_util * indice / (total_pontos - 1)

    def posicao_y(valor):
        return base - altura_util * (valor - minimo) / faixa

        abertura = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}" '
        'role="img" aria-label="Temperatura por cidade">'
    )

    partes = [
        abertura,
        f'<line x1="{MARGEM}" y1="{base}" x2="{LARGURA - MARGEM}" y2="{base}" stroke="#888"/>',
        f'<line x1="{MARGEM}" y1="{MARGEM}" x2="{MARGEM}" y2="{base}" stroke="#888"/>',
        f'<text x="4" y="{MARGEM + 4}" font-size="11" fill="#666">{maximo:.1f} °C</text>',
        f'<text x="4" y="{base}" font-size="11" fill="#666">{minimo:.1f} °C</text>',
    ]

    for indice, (cidade, valores) in enumerate(sorted(series.items())):
        cor = CORES[indice % len(CORES)]
        pontos = " ".join(
            f"{posicao_x(i):.1f},{posicao_y(v):.1f}" for i, v in enumerate(valores)
        )
        partes.append(
            f'<polyline fill="none" stroke="{cor}" stroke-width="2" points="{pontos}"/>'
        )
        for i, valor in enumerate(valores):
            partes.append(
                f'<circle cx="{posicao_x(i):.1f}" cy="{posicao_y(valor):.1f}" '
                f'r="3" fill="{cor}"/>'
            )
        partes.append(
            f'<text x="{MARGEM + 130 * indice}" y="24" font-size="13" '
            f'fill="{cor}">{escape(cidade)}</text>'
        )

    partes.append("</svg>")
    return "\n".join(partes)


def salvar(caminho, svg):
    arquivo = Path(caminho)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(svg, encoding="utf-8")
