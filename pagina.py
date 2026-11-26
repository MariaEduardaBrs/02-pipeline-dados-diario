"""Gera a página HTML com o gráfico e os dados mais recentes."""
from html import escape

ESTILO = """:root { color-scheme: light dark; }
body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; }
h1 { margin-bottom: 0.2rem; }
.sub { margin-top: 0; opacity: 0.75; }
.card { border: 1px solid #8884; border-radius: 12px; padding: 1rem; margin: 1.5rem 0; }
table { border-collapse: collapse; width: 100%; }
th { text-align: left; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.7; }
th, td { padding: 0.6rem 0.5rem; border-bottom: 1px solid #8883; }
td:first-child { font-weight: 600; }
img { display: block; max-width: 100%; height: auto; }
.nota { font-size: 0.9rem; opacity: 0.75; margin-bottom: 0; }
footer { margin-top: 2rem; font-size: 0.9rem; opacity: 0.8; }"""


def ultimos_por_cidade(linhas):
    """Devolve {cidade: linha mais recente}."""
    ultimos = {}
    for linha in sorted(linhas, key=lambda item: item["momento"]):
        ultimos[linha["cidade"]] = linha
    return ultimos


def montar_linha(linha):
    cidade = escape(linha["cidade"])
    temperatura = escape(linha["temperatura_c"])
    umidade = escape(linha["umidade_pct"])
    vento = escape(linha["vento_kmh"])
    return f"<tr><td>{cidade}</td><td>{temperatura} °C</td><td>{umidade}%</td><td>{vento} km/h</td></tr>"


def gerar_html(linhas):
    ultimos = ultimos_por_cidade(linhas)
    if not ultimos:
        raise ValueError("Não há dados para a página.")
    atualizado = escape(max(linha["momento"] for linha in ultimos.values()))
    tabela = "\n".join(montar_linha(linha) for linha in ultimos.values())
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clima por cidade</title>
<style>
{ESTILO}
</style>
</head>
<body>
<h1>Clima por cidade</h1>
<p class="sub">Pipeline diário de dados com GitHub Actions. Última coleta: {atualizado} (horário da API).</p>
<div class="card">
<img src="grafico.svg" alt="Gráfico de temperatura por cidade">
<p class="nota">A coleta roda todo dia por volta das 06:17 (horário de Brasília). As linhas do gráfico aparecem a partir do segundo dia de dados.</p>
</div>
<div class="card">
<table>
<tr><th>Cidade</th><th>Temperatura</th><th>Umidade</th><th>Vento</th></tr>
{tabela}
</table>
</div>
<footer>
<p><a href="https://open-meteo.com/">Weather data by Open-Meteo.com</a> (licença CC BY 4.0).</p>
<p>Código no <a href="https://github.com/MariaEduardaBrs/02-pipeline-dados-diario">GitHub</a>.</p>
</footer>
</body>
</html>
"""
