import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def sincronizar():
    archivo = 'hoquei_data.json'
    
    # 1. Cargamos tus datos actuales para no perderlos
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return # Si hay error no hacemos nada para no borrar

    # 2. Intentamos pillar la clasificación real
    try:
        url = "https://www.hockeypatines.fep.es/league/3150"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        tabla = soup.find('table')
        
        if tabla:
            filas = tabla.find_all('tr')[1:]
            for fila in filas:
                cols = fila.find_all('td')
                if len(cols) >= 10:
                    nombre_fep = cols[1].get_text(strip=True)
                    puntos_fep = int(cols[9].get_text(strip=True))
                    
                    # Actualizamos puntos solo si el equipo ya está en nuestra lista
                    for equipo in data['equipos']:
                        if nombre_fep.lower() in equipo['n'].lower():
                            equipo['pts'] = puntos_fep
        
        data['ultima_actualizacion'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # 3. Guardamos sin borrar categorías
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error sincronització: {e}")

if __name__ == "__main__":
    sincronizar()
