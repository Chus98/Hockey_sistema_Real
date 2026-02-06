import json

def obtener_datos_reales():
    # Esta es la base de datos de tu robot
    equipos = [
        # --- CATALUNYA ---
        {"n": "CP Sant Cugat", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Lliga Plata", "Base"]},
        {"n": "CH Caldes Recam Làser", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Junior"]},
        {"n": "CP Vic", "reg": "CAT", "ok": True, "cats": ["OK Lliga Plata", "Junior", "Juvenil"]},
        {"n": "CP Manlleu", "reg": "CAT", "ok": True, "cats": ["OK Lliga Femenina", "Lliga Plata"]},
        {"n": "Igualada Rigat HC", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "1ª Catalana"]},
        {"n": "CE Noia Freixenet", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Base"]},
        {"n": "CP Calafell", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Base"]},
        {"n": "CP Cambrils", "reg": "CAT", "ok": False, "cats": ["2ª Catalana", "Sènior Femení"]},
        {"n": "CH Riudoms", "reg": "CAT", "ok": False, "cats": ["2ª Catalana", "Infantil"]},
        {"n": "Vila-seca CH", "reg": "CAT", "ok": False, "cats": ["2ª Catalana", "Juvenil"]},
        {"n": "CH Olimpic Reus", "reg": "CAT", "ok": False, "cats": ["2ª Catalana", "3ª Catalana"]},
        {"n": "CH Mataró", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Base"]},
        {"n": "CP Vilafranca", "reg": "CAT", "ok": True, "cats": ["OK Lliga Plata", "Base"]},
        
        # --- ESPAÑA ---
        {"n": "Deportivo Liceo", "reg": "FSP", "ok": True, "cats": ["OK Lliga", "Base Galega"]},
        {"n": "PAS Alcoi", "reg": "ESP", "ok": True, "cats": ["OK Lliga", "Base Valenciana"]},
        {"n": "Hockey Rivas", "reg": "ESP", "ok": True, "cats": ["OK Lliga", "Base Madrid"]},
        {"n": "CP Alcobendas", "reg": "ESP", "ok": True, "cats": ["OK Lliga Plata", "Base"]},
        {"n": "CP Alcorcón", "reg": "ESP", "ok": False, "cats": ["Lliga Madrid", "Base"]},
        {"n": "CP Raspeig", "reg": "ESP", "ok": False, "cats": ["Autonòmica Valenciana", "Base"]},
        {"n": "Alameda de Osuna", "reg": "ESP", "ok": False, "cats": ["Lliga Madrid", "Base"]}
    ]
    return equipos

# El robot guarda todo este volcado en el archivo JSON que lee tu web
try:
    datos = obtener_datos_reales()
    with open('hoquei_data.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("✅ Robot JLS: Datos sincronizados con éxito.")
except Exception as e:
    print(f"❌ Error en el robot: {e}")
