#!/usr/bin/env python3
# geo.py – Graphhopper en español, 2 decimales, salida s/salir, narrativa

import os
import requests

# >>> TU API KEY YA INTEGRADA <<<
TOKEN = os.getenv("GRAPHHOPPER_KEY", "102dbaef-7157-4de5-855d-a21e01ecb9b7")
BASE_URL = "https://graphhopper.com/api/1/route"

def obtener_ruta(origen: str, destino: str):
    """
    origen/destino: 'lat,long'  (ej: '-33.4372,-70.6506')
    """
    params = {
        "point": [origen, destino],
        "vehicle": "car",
        "locale": "es",   # instrucciones en español
        "key": TOKEN
    }
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    if "paths" not in data or not data["paths"]:
        print("No se recibieron rutas. Verifique coordenadas y token.")
        return

    path = data["paths"][0]
    distancia_km = round(path.get("distance", 0) / 1000, 2)   # 2 decimales
    tiempo_min   = round(path.get("time", 0) / 60000, 2)      # 2 decimales

    print("\n=== Resultados del viaje ===")
    print(f"Distancia total: {distancia_km:.2f} km")
    print(f"Tiempo estimado: {tiempo_min:.2f} minutos")

    instrucciones = path.get("instructions", [])
    if not instrucciones:
        print("\nNo hay instrucciones disponibles.")
    else:
        print("\nInstrucciones del viaje:")
        for i, paso in enumerate(instrucciones, start=1):
            print(f" {i:02d}. {paso.get('text','(sin texto)')}")

def main():
    print("=== Planificador de Rutas – Biblioteca Nacional (Graphhopper) ===")
    print("Formato coordenadas: lat,long  (ej: -33.4372,-70.6506)")
    print("Escribe 's' o 'salir' para terminar.")

    while True:
        origen = input("\nIngrese coordenadas de ORIGEN: ").strip()
        if origen.lower() in ("s", "salir"):
            print("Saliendo del programa. ¡Hasta luego!")
            break

        destino = input("Ingrese coordenadas de DESTINO: ").strip()
        if destino.lower() in ("s", "salir"):
            print("Saliendo del programa. ¡Hasta luego!")
            break

        if not TOKEN:
            print("⚠️ No hay API Key configurada. Revise TOKEN.")
            continue

        try:
            obtener_ruta(origen, destino)
        except requests.HTTPError as e:
            print(f"Error HTTP: {e} (revise token/cuota).")
        except requests.RequestException as e:
            print(f"Error de red: {e} (verifique conexión).")
        except Exception as e:
            print(f"Error: {e} (revise formato de coordenadas).")

if __name__ == "__main__":
    main()


