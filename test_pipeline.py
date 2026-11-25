import pipeline

REGISTRO = {
    "cidade": "A",
    "momento": "2026-11-25T12:00",
    "temperatura_c": 25.5,
    "umidade_pct": 60,
    "vento_kmh": 10.2,
}

def test_executar_grava_historice_e_gera_grafico(tmp_path, monkeypatch):
    monkeypath.setattr(pipeline.coleta, "coletar", lambda: [REGISTRO])
    caminho_csv = tmp_path / "dados" / "historico.csv"
    caminho_svg = tmp_path / "site" / "grafico.svg"

    novos = pipeline.executar(caminho_csv, caminho_svg)

    assert novos == 1
    assert caminho_csv.exists()
    assert caminho_svg.read_text(encoding="utf-8").startswith("<svg")
  
def test_executar_duas_vezes_nao_duplica_registros(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline.coleta, "coletar", lambda: [REGISTRO])
    caminho_csv = tmp_path / "historico.csv"
    caminho_svg = tmp_path / "grafico.svg"

    pipeline.executar(caminho_csv, caminho_svg)
    assert pipeline.executar(caminho_csv, caminho_svg) == 0
