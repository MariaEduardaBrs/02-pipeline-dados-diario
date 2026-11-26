"""Gera um gráfico de linhas em SVG com a temperatura de cada cidade."""
import math
from datetime import datetime
from html import escape
from pathlib import Path

LARGURA = 720
ALTURA = 360
MARGEM_ESQ = 60
MARGEM_DIR = 30
MARGEM_TOPO = 50
MARGEM_BASE = 50
FONTE = "system-ui, sans-serif"
CORES = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]
FORMATO_DATA = "%d/%m %H:%M"


def agrupar_por_cidade(linhas):
    """Transforma linhas do CSV em {cidade: [(momento, temperatura)]}."""
    series = {}
    for linha in sorted(linhas, key=lambda item: item["momento"]):
        momento = datetime.fromisoformat(linha["momento"])
        temperatura = float(linha["temperatura_c"])
        series.setdefault(linha["cidade"], []).append((momento, temperatura))
    return series


def limites_y(minimo, maximo):
    """Devolve (base, topo, passo) com 4 divisões inteiras e uma folga."""
    base = math.floor(minimo) - 1
    topo = math.ceil(maximo) + 1
    passo = max(1, math.ceil((topo - base) / 4))
    return base, base + passo * 4, passo


def texto(x, y, conteudo, tamanho=11, cor="#666", ancora="start"):
    rotulo = escape(str(conteudo))
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{tamanho}" fill="{cor}" text-anchor="{ancora}">{rotulo}</text>'


def gerar_svg(series):
    if not series:
        raise ValueError("Não há dados para desenhar.")

    todos = [ponto for pontos in series.values() for ponto in pontos]
    tempos = [momento for momento, _ in todos]
    valores = [valor for _, valor in todos]
    t_min, t_max = min(tempos), max(tempos)
    duracao = (t_max - t_min).total_seconds()
    y_min, y_max, passo = limites_y(min(valores), max(valores))

    largura_util = LARGURA - MARGEM_ESQ - MARGEM_DIR
    altura_util = ALTURA - MARGEM_TOPO - MARGEM_BASE
    base = ALTURA - MARGEM_BASE
    direita = LARGURA - MARGEM_DIR

    def posicao_x(momento):
        if duracao == 0:
            return MARGEM_ESQ + largura_util / 2
        decorrido = (momento - t_min).total_seconds()
        return MARGEM_ESQ + largura_util * decorrido / duracao

    def posicao_y(valor):
        return base - altura_util * (valor - y_min) / (y_max - y_min)

    abertura = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}" font-family="{FONTE}" role="img" aria-label="Temperatura por cidade">'
    partes = [abertura]

    for indice in range(5):
        valor = y_min + passo * indice
        y = posicao_y(valor)
        partes.append(f'<line x1="{MARGEM_ESQ}" y1="{y:.1f}" x2="{direita}" y2="{y:.1f}" stroke="#888" stroke-opacity="0.25"/>')
        partes.append(texto(MARGEM_ESQ - 8, y + 4, f"{valor} °C", ancora="end"))

    partes.append(f'<line x1="{MARGEM_ESQ}" y1="{MARGEM_TOPO}" x2="{MARGEM_ESQ}" y2="{base}" stroke="#888"/>')

    if duracao == 0:
        partes.append(texto(posicao_x(t_min), base + 22, t_min.strftime(FORMATO_DATA), ancora="middle"))
    else:
        partes.append(texto(posicao_x(t_min), base + 22, t_min.strftime(FORMATO_DATA), ancora="start"))
        partes.append(texto(posicao_x(t_max), base + 22, t_max.strftime(FORMATO_DATA), ancora="end"))

    for indice, (cidade, pontos) in enumerate(sorted(series.items())):
        cor = CORES[indice % len(CORES)]
        coordenadas = " ".join(f"{posicao_x(m):.1f},{posicao_y(v):.1f}" for m, v in pontos)
        partes.append(f'<polyline fill="none" stroke="{cor}" stroke-width="2" points="{coordenadas}"/>')
        for momento, valor in pontos:
            x = posicao_x(momento)
            y = posicao_y(valor)
            partes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{cor}"/>')
        partes.append(texto(MARGEM_ESQ + 130 * indice, 28, cidade, tamanho=13, cor=cor))

    partes.append("</svg>")
    return "\n".join(partes)


def salvar(caminho, svg):
    arquivo = Path(caminho)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(svg, encoding="utf-8")
