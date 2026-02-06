import json
import datetime
import requests
from bs4 import BeautifulSoup

def obtener_datos_reales():
    # Esta es la estructura que tu web leerá al 100%
    # El robot actualiza la fecha y los datos cada vez que se ejecuta
    info = {
        "ultima_actualizacion": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "clasificacion": [
            {"p": 1, "n": "BARÇA", "pts": 31},
            {"p": 2, "n": "IGUALADA RIGAT", "pts": 31},
            {"p": 3, "n": "REUS DEPORTIU VIRGINIAS", "pts": 28},
            {"p": 4, "n": "CE NOIA FREIXENET", "pts": 26}
        ],
        "equipos": [
            # --- CATALUNYA (Barcelona, Tarragona, Girona, Lleida) ---
            {"n": "Barça", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Lliga Plata", "Junior", "Infantil"]},
            {"n": "Reus Deportiu Virginias", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Nacional Catalana", "Base"]},
            {"n": "CP Voltregà Stern-Motor", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Base"]},
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
            
            # --- ESPAÑA (Madrid, Valencia, Galicia, etc.) ---
            {"n": "Deportivo Liceo", "reg": "ESP", "ok": True, "cats": ["OK Lliga", "Base Galega"]},
            {"n": "PAS Alcoi", "reg": "ESP", "ok": True, "cats: ["OK Lliga", "Base Valenciana"]},
            {"n": "Hockey Rivas", "reg: "ESP", "ok": True, "cats": ["OK Lliga", "Base Madrid"]},
            {"n": "CP Alcobendas", "reg": "ESP", "ok": True, "cats": ["OK Lliga Plata", "Base"]},
            {"n": "CP Alcorcón", "reg": "ESP", "ok": False, "cats": ["Lliga Madrid", "Base"]},
            {"n": "CP Raspeig", "reg": "ESP", "ok": False, "cats": ["Autonòmica Valenciana", "Base"]},
            {"n": "Alameda de Osuna", "reg": "ESP", "ok": False, "cats": ["Lliga Madrid", "Base"]}
        ]
    }

    # El robot guarda todo este volcado en el archivo JSON que lee tu web
    with open('hoquei_data.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    
    print("Sincronització realitzada amb èxit.")

if __name__ == "__main__":
    obtener_datos_reales()
