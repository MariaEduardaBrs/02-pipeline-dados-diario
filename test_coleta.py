import json

import pytest

import coleta

RESPOSTA_FALSA = {
    "current": {
        "time": "2026-11-25T12:00",
        "temperature_2m": 25.5,
        "relative_humidity_2m": 60,
        "wind_speed_10m": 10.2,
    }
}


class RespostaHttpFalsa:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(RESPOSTA_FALSA).encode("utf-8")


def test_montar_url_tem_coordenadas_e_campos():
    url = coleta.montar_url(-23.55, -46.63)
    assert url.startswith("https://api.open-meteo.com/v1/forecast?")
    assert "latitude=-23.55" in url
    assert "temperature_2m" in url


def test_extrair_registro():
    registro = coleta.extrair_registro("Cidade Teste", RESPOSTA_FALSA)
    assert registro["cidade"] == "Cidade Teste"
    assert registro["temperatura_c"] == 25.5
    assert registro["umidade_pct"] == 60


def test_extrair_registro_sem_current_gera_erro():
    with pytest.raises(ValueError):
        coleta.extrair_registro("X", {})


def test_buscar_le_o_json_da_resposta(monkeypatch):
    monkeypatch.setattr(
        coleta.urllib.request, "urlopen", lambda url, timeout: RespostaHttpFalsa()
    )
    assert coleta.buscar(0, 0) == RESPOSTA_FALSA


def test_coletar_junta_todas_as_cidades(monkeypatch):
    monkeypatch.setattr(coleta, "buscar", lambda latitude, longitude: RESPOSTA_FALSA)
    registros = coleta.coletar({"A": (0, 0), "B": (1, 1)})
    assert [r["cidade"] for r in registros] == ["A", "B"]
