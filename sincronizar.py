import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def sincronizar_real():
    url_fep = "https://www.hockeypatines.fep.es/league/3150"
    archivo_json = 'hoquei_data.json'
    
    try:
        # 1. Cargar tus datos actuales (equipos y categorías)
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos_app = json.load(f)
        
        # 2. Leer la web de la federación
        response = requests.get(url_fep, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        
        if tabla:
            filas = tabla.find_all('tr')[1:]
            for fila in filas:
                cols = fila.find_all('td')
                if len(cols) >= 10:
                    nombre_web = cols[1].get_text(strip=True)
                    puntos_web = int(cols[9].get_text(strip=True))
                    
                    # 3. Buscar el equipo en tu lista y actualizar SOLO los puntos
                    for equipo in datos_app['equipos']:
                        # Comprobación flexible de nombres
                        if nombre_web.lower() in equipo['n'].lower() or equipo['n'].lower() in nombre_web.lower():
                            equipo['pts'] = puntos_web

        datos_app['ultima_actualizacion'] = datetime.now().strftime("%d/%m/%Y %H:%M")

        # 4. Guardar los cambios manteniendo todo lo demás
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos_app, f, ensure_ascii=False, indent=4)
        
        print("✅ Sincronización 100% Real Completada")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sincronizar_real()
