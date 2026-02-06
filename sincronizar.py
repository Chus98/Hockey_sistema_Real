import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def obtener_datos_oficiales():
    url = "https://www.hockeypatines.fep.es/league/3150"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    equipos_reales = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        
        if tabla:
            filas = tabla.find_all('tr')[1:] # Saltamos la cabecera
            for fila in filas:
                cols = fila.find_all('td')
                if len(cols) >= 10:
                    nombre = cols[1].get_text(strip=True)
                    pts = cols[9].get_text(strip=True)
                    
                    equipos_reales.append({
                        "n": nombre,
                        "pts": int(pts) if pts.isdigit() else 0,
                        "reg": "ESP",
                        "ok": True,
                        "cats": ["OK LLIGA 25/26"]
                    })
        return equipos_reales
    except Exception as e:
        print(f"Error: {e}")
        return []

# Generamos el archivo final
datos_fep = obtener_datos_oficiales()
resultado = {
    "ultima_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "equipos": datos_fep,
    "reglamento_url": "https://fep.es/federacion/reglamentos"
}

with open('hoquei_data.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, ensure_ascii=False, indent=4)
print("✅ Sincronización finalizada con éxito")
