import pytest

import pagina

LINHAS = [
    {
        "cidade": "A",
        "momento": "2026-11-25T12:00",
        "temperatura_c": "25.0",
        "umidade_pct": "60",
        "vento_kmh": "10.0",
    },
    {
        "cidade": "A",
        "momento": "2026-11-26T12:00",
        "temperatura_c": "27.0",
        "umidade_pct": "55",
        "vento_kmh": "12.0",
    },
]


def test_ultimos_por_cidade_pega_o_mais_recente():
    ultimos = pagina.ultimos_por_cidade(LINHAS)
    assert ultimos["A"]["temperatura_c"] == "27.0"


def test_gerar_html_tem_creditos_tabela_e_grafico():
    conteudo = pagina.gerar_html(LINHAS)
    assert "Weather data by Open-Meteo.com" in conteudo
    assert "<td>27.0 °C</td>" in conteudo
    assert 'src="grafico.svg"' in conteudo


def test_gerar_html_escapa_o_nome_da_cidade():
    linhas = [dict(LINHAS[0], cidade="<b>X</b>")]
    conteudo = pagina.gerar_html(linhas)
    assert "<b>X</b>" not in conteudo
    assert "&lt;b&gt;X&lt;/b&gt;" in conteudo


def test_gerar_html_sem_dados_gera_erro():
    with pytest.raises(ValueError):
        pagina.gerar_html([])
