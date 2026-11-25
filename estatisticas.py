"""Funções de estatística usadas pelo pipeline."""


def media(valores):
    """Devolve a média simples de uma lista de números."""
    if not valores:
        raise ValueError("A lista de valores está vazia.")
    return sum(valores) / len(valores)
