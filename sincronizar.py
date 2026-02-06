import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def sincronizar_oficial():
    # Link oficial de clasificación que proporcionaste
    url = "https://www.hockeypatines.fep.es/league/3150"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Cargamos los datos locales para mantener las categorías
        with open('hoquei_data.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)

        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Localizamos la tabla de clasificación
        tabla = soup.find('table')
        if tabla:
            filas = tabla.find_all('tr')[1:] # Omitimos cabecera
            for fila in filas:
                cols = fila.find_all('td')
                if len(cols) >= 10:
                    # Nombre en la web de la federación
                    nombre_fep = cols[1].get_text(strip=True)
                    # Puntos en la columna correspondiente
                    puntos_fep = int(cols[9].get_text(strip=True))
                    
                    # Buscamos coincidencia en nuestra lista
                    for equipo in datos['equipos']:
                        # Comparamos nombres (ej: "Barça" está contenido en "FC Barcelona")
                        if equipo['n'].lower() in nombre_fep.lower() or nombre_fep.lower() in equipo['n'].lower():
                            equipo['pts'] = puntos_fep

        datos['ultima_actualizacion'] = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Guardamos la actualización real
        with open('hoquei_data.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print("✅ Sincronització real amb FEP finalitzada.")

    except Exception as e:
        print(f"❌ Error de conexió: {e}")

if __name__ == "__main__":
    sincronizar_oficial()
