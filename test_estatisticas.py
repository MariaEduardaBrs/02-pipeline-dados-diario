import pytest

from estatisticas import media


def test_media_de_valores_simples():
    assert media([2, 4, 6]) == 4


def test_media_de_lista_vazia_gera_erro():
    with pytest.raises(ValueError):
        media([])
