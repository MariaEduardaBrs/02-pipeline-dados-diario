"""Coleta o clima atual de algumas cidades pela API pública Open-Meteo."""
import json
import urllib.parse
import urllib.request

URL_BASE = "https://api.open-meteo.com/v1/forecast"
CAMPOS = "temperature_2m,relative_humidity_2m,wind_speed_10m"

CIDADES = {
    "São Paulo": (-23.55, -46.63),
    "Salvador": (-12.97, -38.50),
    "Brasília": (-15.78, -47.93),
}


def montar_url(latitude, longitude):
    parametros = urllib.parse.urlencode(
        {"latitude": latitude, "longitude": longitude, "current": CAMPOS}
    )
    return f"{URL_BASE}?{parametros}"


def buscar(latitude, longitude):
    url = montar_url(latitude, longitude)
    with urllib.request.urlopen(url, timeout=10) as resposta:
        return json.load(resposta)


def extrair_registro(cidade, resposta):
    if "current" not in resposta:
        raise ValueError("Resposta sem o campo 'current'.")
    atual = resposta["current"]
    return {
        "cidade": cidade,
        "momento": atual["time"],
        "temperatura_c": atual["temperature_2m"],
        "umidade_pct": atual["relative_humidity_2m"],
        "vento_kmh": atual["wind_speed_10m"],
    }


def coletar(cidades=CIDADES):
    registros = []
    for cidade, (latitude, longitude) in cidades.items():
        registros.append(extrair_registro(cidade, buscar(latitude, longitude)))
    return registros


if __name__ == "__main__":
    for registro in coletar():
        print(registro)
