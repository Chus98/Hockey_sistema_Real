import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURACIÓN DE LIGAS (Rastreo Senior)
# ==========================================
LIGAS = [
    # ESPAÑA (FEP)
    {"url": "https://www.hockeypatines.fep.es/league/3150", "cat": "OK LLIGA", "region": "ESP", "es_ok": True},
    {"url": "https://www.hockeypatines.fep.es/league/3158", "cat": "OK LLIGA PLATA NORD", "region": "ESP", "es_ok": False},
    {"url": "https://www.hockeypatines.fep.es/league/3159", "cat": "OK LLIGA PLATA SUD", "region": "ESP", "es_ok": False},
    
    # CATALUNYA (FCP) - Añade aquí los links de 1a, 2a, 3a Catalana que quieras
    {"url": "http://www.fcpatinatge.cat/ca/competicio/hoquei-patins/nacional-catalana-masculina/classificacio", "cat": "NACIONAL CATALANA", "region": "CAT", "es_ok": False},
    {"url": "http://www.fcpatinatge.cat/ca/competicio/hoquei-patins/1a-catalana-masculina/classificacio", "cat": "1ª CATALANA", "region": "CAT", "es_ok": False},
]

# ⛔ CLUBES SIN CANTERA (Excepciones)
# Estos clubes NO recibirán las categorías inferiores automáticas.
CLUBES_SIN_BASE = ["CN REUS PLOMS"]

# 👶 LA ESCALERA COMPLETA (De arriba a abajo)
# Estas son las categorías que se añadirán a los clubes normales.
CATEGORIAS_BASE = [
    "Júnior",
    "Juvenil",
    "Infantil",
    "Aleví",
    "Benjamí",
    "Prebenjamí",
    "Escola"
]

# ==========================================
# 🚀 MOTOR DEL SCRIPT
# ==========================================

def normalizar_nombre(nombre):
    """Limpia nombres para evitar duplicados"""
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
    """Si el club es normal, le añade toda la estructura de base"""
    
    # 1. Comprobamos si es una excepción (Ej: Reus Ploms)
    for excepcion in CLUBES_SIN_BASE:
        if excepcion in nombre_club:
            # Si es excepción, NO tocamos nada (se queda solo con lo que tenga)
            return cats_actuales

    # 2. Si no es excepción, añadimos la escalera completa si no la tiene ya
    for cat_base in CATEGORIAS_BASE:
        if cat_base not in cats_actuales:
            cats_actuales.append(cat_base)
            
    return cats_actuales

def sincronizar_todo():
    print(f"🚀 INICIANDO ACTUALIZACIÓN TOTAL ({datetime.now().strftime('%H:%M:%S')})")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Cargar JSON o crear nuevo
    try:
        with open('hoquei_data.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except:
        datos = {"equipos": []}

    equipos_map = {e['n']: e for e in datos['equipos']}
    
    # RASTREO DE LIGAS
    for liga in LIGAS:
        try:
            print(f"📡 Escanejant: {liga['cat']}...")
            r = requests.get(liga['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            filas = soup.find_all('tr')[1:]
            
            for fila in filas:
                cols = fila.find_all('td')
                if not cols: continue
                
                # Extracción genérica de nombre y puntos
                textos = [c.get_text(strip=True) for c in cols]
                nombre_raw = ""
                puntos = 0
                
                # Buscar nombre (texto largo) y puntos (dígitos al final)
                for t in textos:
                    if len(t) > 4 and not t.isdigit():
                        nombre_raw = t
                        break
                for t in reversed(textos):
                    if t.isdigit():
                        puntos = int(t)
                        break
                
                if not nombre_raw: continue
                
                nombre = normalizar_nombre(nombre_raw)
                
                # Crear o actualizar
                if nombre not in equipos_map:
                    equipos_map[nombre] = {
                        "n": nombre, "pts": 0, "reg": liga['region'],
                        "ok": False, "cat_label": liga['cat'], "cats": []
                    }
                
                e = equipos_map[nombre]
                if e['pts'] < puntos: e['pts'] = puntos # Maximos puntos
                
                if liga['es_ok']: 
                    e['ok'] = True
                    e['cat_label'] = "OK LLIGA"
                
                if liga['cat'] not in e['cats']:
                    e['cats'].append(liga['cat'])

        except Exception as ex:
            print(f"⚠️ Error en {liga['cat']}: {ex}")

    # APLICAR LÓGICA DE CANTERA
    print("✨ Generando estructura de categorías (Júnior a Escola)...")
    lista_final = []
    
    for nombre, equipo in equipos_map.items():
        # Aquí ocurre la magia: Se añaden todas las categorías
        equipo['cats'] = asignar_cantera_completa(nombre, equipo['cats'])
        lista_final.append(equipo)

    # Ordenar y Guardar
    lista_final.sort(key=lambda x: x['pts'], reverse=True)
    datos['equipos'] = lista_final
    datos['ultima_actualizacion'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    with open('hoquei_data.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ FINALIZADO. Equipos actualizados: {len(lista_final)}")

if __name__ == "__main__":
    sincronizar_todo()
