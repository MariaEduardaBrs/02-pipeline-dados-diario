"""Gera a pagina HTML com o gráfico e os dados mais recentes"""

from html import escape

ESTILO = """:root { color-scheme: light dark;}
body {font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5;}
table { border-collapse: collapse; width: 100%; }
th, td { border-bottom: 1px solid #8884; padding: 0.4rem; text-align: left; }
img { max-width: 100%; height: auto; }
footer { margin-top:2rem; font-size: 0.9rem; opacity: 0.8; }"""

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
    return f"<tr><t>{cidade}</td><td>{temperatura} °C</td><td>{umidade}%</td><td>{vento} km/h</td></tr>"

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
<p>Pipeline diário de dados com GitHub Actions.Última coleta: {atualizado} (horário da API). </p>
<img src="grafico.svg" alt="Gráfico de temperatura por cidade">
<table>
<tr><th>Cidade</th><th>Temperatura</th><th>Umidade</th><th>Vento</th></tr>
{tabela}
</table>
<footer>
<p><a href="https://open-meteo.com/">Weather data by Open-Meteo.com</a> (licença CC BY 4.0).</p>
<p>Código no <a href="https://github.com/MariaEduardaBrs/02-pipeline-dados-diario">GitHub</a>.</p>
</footer>
</body>
</html>
"""
