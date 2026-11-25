"""Orquestra o pipeline: coleta, grava o histórico e gera o gráfico."""
import coleta
import grafico
import historico

CAMINHO_HISTORICO = "dados/historico.csv"
CAMINHO_GRAFICO = "site/grafico.svg"

def executar(caminho_historico=CAMINHO_HISTORICO, caminho_grafico=CAMINHO_GRAFICO):
    registros = coleta.coletar()
    novos = historico.adicionar(caminho_historico, registros)
    series = grafico.agrupar_por_cidade(historico.ler(caminho_historico))
    grafico.salvar(caminho_grafico, grafico.gerar_svg(series))
    return novos

if __name__ == "__main__":
    print(f"Registros novos: {executar()}")
