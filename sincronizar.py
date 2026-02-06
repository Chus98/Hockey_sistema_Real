# Parte final de sincronizar.py
datos_finales = {
    "ultima_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "equipos": obtener_clasificacion_real(), # Aquí están los puntos reales de la FEP
    "reglamento_url": "https://fep.es/federacion/reglamentos" # Enlace siempre vivo
}

with open('hoquei_data.json', 'w', encoding='utf-8') as f:
    json.dump(datos_finales, f, ensure_ascii=False, indent=4)
