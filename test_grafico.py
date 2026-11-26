from datetime import datetime, timedelta

import pytest

import grafico

LINHAS = [
    {"cidade": "A", "momento": "2026-11-26T12:00", "temperatura_c": "27.0"},
    {"cidade": "A", "momento": "2026-11-25T12:00", "temperatura_c": "25.0"},
    {"cidade": "B", "momento": "2026-11-25T12:00", "temperatura_c": "30.5"},
]


def serie(*valores):
    inicio = datetime(2026, 11, 25, 12, 0)
    return [(inicio + timedelta(days=i), v) for i, v in enumerate(valores)]


def test_agrupar_ordena_por_momento_e_converte_os_tipos():
    series = grafico.agrupar_por_cidade(LINHAS)
    assert series["A"] == [
        (datetime(2026, 11, 25, 12, 0), 25.0),
        (datetime(2026, 11, 26, 12, 0), 27.0),
    ]
    assert series["B"] == [(datetime(2026, 11, 25, 12, 0), 30.5)]


def test_limites_y_dao_folga_e_passo_inteiro():
    assert grafico.limites_y(20.4, 29.7) == (19, 31, 3)


def test_limites_y_com_valores_iguais():
    assert grafico.limites_y(20.0, 20.0) == (19, 23, 1)


def test_gerar_svg_tem_uma_linha_por_cidade():
    svg = grafico.gerar_svg({"A": serie(25.0, 27.0), "B": serie(30.0, 29.0)})
    assert svg.startswith("<svg")
    assert svg.count("<polyline") == 2
    assert svg.endswith("</svg>")


def test_gerar_svg_mostra_datas_e_fonte():
    svg = grafico.gerar_svg({"A": serie(25.0, 27.0)})
    assert "25/11 12:00" in svg
    assert "26/11 12:00" in svg
    assert "font-family" in svg


def test_gerar_svg_escapa_o_nome_da_cidade():
    svg = grafico.gerar_svg({"<b>X</b>": serie(20.0, 21.0)})
    assert "<b>" not in svg
    assert "&lt;b&gt;" in svg


def test_gerar_svg_aceita_um_unico_ponto():
    svg = grafico.gerar_svg({"A": serie(20.0)})
    assert "<circle" in svg


def test_gerar_svg_aceita_valores_iguais():
    svg = grafico.gerar_svg({"A": serie(20.0, 20.0)})
    assert "<polyline" in svg


def test_gerar_svg_sem_dados_gera_erro():
    with pytest.raises(ValueError):
        grafico.gerar_svg({})


def test_salvar_cria_pasta_e_arquivo(tmp_path):
    caminho = tmp_path / "site" / "grafico.svg"
    grafico.salvar(caminho, "<svg></svg>")
    assert caminho.read_text(encoding="utf-8") == "<svg></svg>"
