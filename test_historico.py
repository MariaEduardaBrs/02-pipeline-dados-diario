import historico

REGISTRO = {
    "cidade": "A",
    "momento": "2026-11-25T12:00",
    "temperatura_c": 25.5,
    "umidade_pct": 60,
    "vento_kmh": 10.2,
}


def test_ler_arquivo_inexistente_devolve_lista_vazia(tmp_path):
    assert historico.ler(tmp_path / "nao_existe.csv") == []


def test_adicionar_cria_arquivo_com_cabecalho(tmp_path):
    caminho = tmp_path / "dados" / "historico.csv"
    assert historico.adicionar(caminho, [REGISTRO]) == 1
    linhas = historico.ler(caminho)
    assert linhas[0]["cidade"] == "A"
    assert linhas[0]["temperatura_c"] == "25.5"


def test_adicionar_nao_duplica_o_mesmo_momento(tmp_path):
    caminho = tmp_path / "historico.csv"
    historico.adicionar(caminho, [REGISTRO])
    assert historico.adicionar(caminho, [REGISTRO]) == 0
    assert len(historico.ler(caminho)) == 1


def test_adicionar_acrescenta_momento_novo(tmp_path):
    caminho = tmp_path / "historico.csv"
    historico.adicionar(caminho, [REGISTRO])
    outro = dict(REGISTRO, momento="2026-11-26T12:00")
    assert historico.adicionar(caminho, [outro]) == 1
    assert len(historico.ler(caminho)) == 2
