import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def obtener_datos_fep():
    # URL de la clasificación oficial que me has pasado
    url_clasificacion = "https://www.hockeypatines.fep.es/league/3150"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    equipos_vivos = []
    
    try:
        # El robot entra en la web de la federación
        response = requests.get(url_clasificacion, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos la tabla de clasificación
        tabla = soup.find('table')
        if not tabla:
            print("⚠️ No s'ha trobat la tabla a la web de la FEP")
            return []

        filas = tabla.find_all('tr')
        
        for fila in filas[1:]:  # Saltamos la cabecera de la tabla
            cols = fila.find_all('td')
            if len(cols) >= 10:
                # Extraemos nombre y puntos reales
                nombre = cols[1].get_text(strip=True)
                # El punto suele estar en la columna 9 o 10 dependiendo de la web
                puntos = cols[9].get_text(strip=True)
                
                equipos_vivos.append({
                    "n": nombre,
                    "pts": int(puntos) if puntos.isdigit() else 0,
                    "reg": "ESP",
                    "ok": True,
                    "cats": ["OK LLIGA 25/26"]
                })
        
        # Ordenamos por puntos (el que tiene más, arriba)
        equipos_vivos.sort(key=lambda x: x['pts'], reverse=True)
        return equipos_vivos

    except Exception as e:
        print(f"❌ Error durant la sincronització: {e}")
        return []

def ejecutar_robot():
    print("🤖 Iniciant robot de sincronització oficial...")
    
    equipos = obtener_datos_fep()
    
    # Estructura final del JSON que leerá tu index.html
    datos_finales = {
        "ultima_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "equipos": equipos,
        "reglamento_url": "https://fep.es/federacion/reglamentos"
    }
    
    # Guardamos el archivo hoquei_data.json
    with open('hoquei_data.json', 'w', encoding='utf-8') as f:
        json.dump(datos_finales, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Sincronitzats {len(equipos)} equips amb dades reals.")

if __name__ == "__main__":
    ejecutar_robot()
