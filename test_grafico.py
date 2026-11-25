import pytest

import grafico

LINHAS = [
  {"cidade": "A", "momento": "2026-11-26T12:00", "temperatura_c": "27.0"},
  {"cidade": "A", "momento": "2026-11-25T12:00", "temperatura_c": "25.0"},
  {"cidade": "B", "momento": "2026-11-25T12:00", "temperatura_c": "30.5"},
]

def test_agrupar_ordena_por_momento_e_converte_para_numero();
 series = grafico.agrupar_por_cidade(LINHAS)
 assert series["A"] == [25.0, 27.0]
 assert series["B"] == [30.5]

def test_gerar_svg_tem_uma_linha_por_cidade();
 svg = grafico.gerar_svg({"A": [25.0, 27.0], "B": [30.0, 29.0]})
 assert svg.startswith("<svg")
 assert svg.count("<polyline") == 2
 assert svg.endswith("</svg>")

def test_gerar_svg_escapa_o_nome_da_cidade();
 svg = grafico.gerar_svg({"<b>X</b>": [20.0, 21.0]})
 assert "<b>" not in svg
 assert "&lt;b&gt;" in svg

def test_gerar_svg_aceita_um_unico_ponto();
 svg = grafico.gerar_svg({"A": [20.0]})
 assert "<circle" in svg

def test_gerar_svg_aceita_valores_iguais();
 svg = grafico.gerar_svg({"A": [20.0, 20.0]})
 assert "<polyline" in svg

def test_gerar_svg_sem_dados_gera_erro();
 with pytest.raises(ValueError):
   grafico.gerar_svg({})

def test_salvar_cria_pasta_e_arquivo(tmp_path):
  caminho = tmp_path / "site" / "grafico.svg"
  grafico.salvar(caminho, "<svg></svg>")
  assert caminho.read_text(enconding="utf-8") == "<svg></svg>"
