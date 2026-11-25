"""Guarda e lê o histórico de registros em um arquivo CSV."""
import csv
from pathlib import Path

COLUNAS = ["cidade", "momento", "temperatura_c", "umidade_pct", "vento_kmh"]


def ler(caminho):
    arquivo = Path(caminho)
    if not arquivo.exists():
        return []
    with arquivo.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def adicionar(caminho, registros):
    """Acrescenta só os registros novos e devolve quantos foram gravados."""
    arquivo = Path(caminho)
    vistos = {(r["cidade"], r["momento"]) for r in ler(arquivo)}
    novos = [r for r in registros if (r["cidade"], r["momento"]) not in vistos]
    if not novos:
        return 0
    escrever_cabecalho = not arquivo.exists()
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with arquivo.open("a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS)
        if escrever_cabecalho:
            escritor.writeheader()
        escritor.writerows(novos)
    return len(novos)
