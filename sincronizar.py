import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def obtener_datos_reales():
    url_fep = "https://www.hockeypatines.fep.es/league/3150"
    headers = {'User-Agent': 'Mozilla/5.0'}
    equipos_extraidos = []
    
    try:
        response = requests.get(url_fep, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        
        if tabla:
            filas = tabla.find_all('tr')[1:] # Saltamos cabecera
            for fila in filas:
                cols = fila.find_all('td')
                if len(cols) >= 10:
                    nombre = cols[1].get_text(strip=True)
                    # Extraemos los puntos reales de la columna oficial
                    pts_reales = cols[9].get_text(strip=True)
                    
                    equipos_extraidos.append({
                        "n": nombre,
                        "pts": int(pts_reales) if pts_reales.isdigit() else 0,
                        "reg": "ESP",
                        "ok": True,
                        "cats": ["OK LLIGA 25/26"]
                    })
        return equipos_extraidos
    except Exception as e:
        print(f"Error FEP: {e}")
        return []

# Ejecución y guardado
datos = obtener_datos_reales()
output = {
    "ultima_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "equipos": datos,
    "reglamento_url": "https://fep.es/federacion/reglamentos"
}

with open('hoquei_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
