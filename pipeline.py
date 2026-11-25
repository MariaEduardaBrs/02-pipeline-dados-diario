"""Orquestra o pipeline: coleta, grava o histórico, gera gráfico e página."""
from pathlib import Path

import coleta
import grafico
import historico
import pagina

CAMINHO_HISTORICO = "dados/historico.csv"
CAMINHO_GRAFICO = "site/grafico.svg"


def executar(caminho_historico=CAMINHO_HISTORICO, caminho_grafico=CAMINHO_GRAFICO):
    registros = coleta.coletar()
    novos = historico.adicionar(caminho_historico, registros)
    linhas = historico.ler(caminho_historico)

    series = grafico.agrupar_por_cidade(linhas)
    grafico.salvar(caminho_grafico, grafico.gerar_svg(series))

    pasta = Path(caminho_grafico).parent
    (pasta / "index.html").write_text(pagina.gerar_html(linhas), encoding="utf-8")
    return novos


if __name__ == "__main__":
    print(f"Registros novos: {executar()}")
