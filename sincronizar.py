import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def actualizar_puntos():
    url = "https://www.hockeypatines.fep.es/league/3150"
    headers = {'User-Agent': 'Mozilla/5.0'}
    equipos_puntos = []
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        tabla = soup.find('table')
        if tabla:
            for fila in tabla.find_all('tr')[1:]:
                cols = fila.find_all('td')
                if len(cols) >= 10:
                    nombre = cols[1].get_text(strip=True)
                    pts = cols[9].get_text(strip=True)
                    equipos_puntos.append({"n": nombre, "pts": int(pts) if pts.isdigit() else 0})
        
        output = {
            "ultima_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "equipos": equipos_puntos
        }
        with open('hoquei_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print("✅ Puntos actualizados.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    actualizar_puntos()
