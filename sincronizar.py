import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURACIÓN DE LIGAS
# ==========================================
LIGAS = [
    {"url": "https://www.hockeypatines.fep.es/league/3150", "cat": "OK LLIGA", "region": "ESP", "es_ok": True},
    {"url": "https://www.hockeypatines.fep.es/league/3158", "cat": "OK LLIGA PLATA NORD", "region": "ESP", "es_ok": False},
    {"url": "https://www.hockeypatines.fep.es/league/3159", "cat": "OK LLIGA PLATA SUD", "region": "ESP", "es_ok": False},
    {"url": "http://www.fcpatinatge.cat/ca/competicio/hoquei-patins/nacional-catalana-masculina/classificacio", "cat": "NACIONAL CATALANA", "region": "CAT", "es_ok": False},
    {"url": "http://www.fcpatinatge.cat/ca/competicio/hoquei-patins/1a-catalana-masculina/classificacio", "cat": "1ª CATALANA", "region": "CAT", "es_ok": False},
    {"url": "http://www.fcpatinatge.cat/ca/competicio/hoquei-patins/2a-catalana-masculina-grup-b/classificacio", "cat": "2ª CATALANA", "region": "CAT", "es_ok": False}
]

CLUBES_SIN_BASE = ["CN REUS PLOMS"]
CATEGORIAS_BASE = ["Júnior", "Juvenil", "Infantil", "Aleví", "Benjamí", "Prebenjamí", "Escola"]

def normalizar_nombre(nombre):
    nombre = nombre.upper().strip()
    reemplazos = {
        "CLUB PATÍ": "CP", "CLUB PATIN": "CP", "C.P.": "CP",
        "HOCKEY CLUB": "HC", "H.C.": "HC", "C.H.": "CH", "CLUB D'HOQUEI": "CH",
        "SECCIÓ ESPORTIVA": "SE", "UNIO ESPORTIVA": "UE"
    }
    for old, new in reemplazos.items():
        nombre = nombre.replace(old, new)
    return " ".join(nombre.split())

def asignar_cantera_completa(nombre_club, cats_actuales):
    for excepcion in CLUBES_SIN_BASE:
        if excepcion in nombre_club: return cats_actuales
    for cat_base in CATEGORIAS_BASE:
        if cat_base not in cats_actuales: cats_actuales.append(cat_base)
    return cats_actuales

def sincronizar_todo():
    print(f"🚀 INICIANDO ACTUALIZACIÓN TOTAL CON EMBLEMAS ({datetime.now().strftime('%H:%M:%S')})")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        with open('hoquei_data.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except:
        datos = {"equipos": []}

    equipos_map = {e['n']: e for e in datos['equipos']}
    
    for liga in LIGAS:
        try:
            print(f"📡 Escaneando: {liga['cat']}...")
            r = requests.get(liga['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Buscamos las filas de la tabla
            filas = soup.find_all('tr')
            
            for fila in filas:
                cols = fila.find_all('td')
                if len(cols) < 3: continue
                
                # --- EXTRACCIÓN DEL EMBLEMA ---
                img_tag = fila.find('img')
                url_emblema = ""
                if img_tag and img_tag.get('src'):
                    url_emblema = img_tag['src']
                    # Completar URL si es relativa
                    if url_emblema.startswith('/'):
                        base = "https://www.hockeypatines.fep.es" if "fep.es" in liga['url'] else "http://www.fcpatinatge.cat"
                        url_emblema = base + url_emblema
                
                # --- EXTRACCIÓN DE TEXTOS ---
                textos = [c.get_text(strip=True) for c in cols]
                nombre_raw = ""
                puntos = 0
                
                # Identificar nombre (texto largo no numérico)
                for t in textos:
                    if len(t) > 3 and not t.replace('.','').isdigit():
                        nombre_raw = t
                        break
                
                # Identificar puntos (último número de la fila)
                for t in reversed(textos):
                    if t.isdigit():
                        puntos = int(t)
                        break
                
                if not nombre_raw: continue
                nombre = normalizar_nombre(nombre_raw)
                
                # Crear o actualizar equipo
                if nombre not in equipos_map:
                    equipos_map[nombre] = {
                        "n": nombre, "pts": 0, "reg": liga['region'],
                        "ok": False, "cat_label": liga['cat'], "cats": [],
                        "img": url_emblema # Nueva propiedad para el logo
                    }
                
                e = equipos_map[nombre]
                e['pts'] = puntos
                # Actualizar logo solo si lo encontramos
                if url_emblema: e['img'] = url_emblema
                
                if liga['es_ok']: 
                    e['ok'] = True
                    e['cat_label'] = "OK LLIGA"
                
                if liga['cat'] not in e['cats']:
                    e['cats'].append(liga['cat'])

        except Exception as ex:
            print(f"⚠️ Error en {liga['cat']}: {ex}")

    # Procesar canteras y limpiar
    lista_final = []
    for nombre, equipo in equipos_map.items():
        equipo['cats'] = asignar_cantera_completa(nombre, equipo['cats'])
        lista_final.append(equipo)

    lista_final.sort(key=lambda x: x['pts'], reverse=True)
    datos['equipos'] = lista_final
    datos['ultima_actualizacion'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    with open('hoquei_data.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ FINALIZADO. Equipos con emblemas actualizados: {len(lista_final)}")

if __name__ == "__main__":
    sincronizar_todo()
