import json
import datetime

# Este robot simula la extracción de las webs que me pasaste
# Cada vez que corre, genera el archivo hoquei_data.json
def update():
    info = {
        "ultima_actualizacion": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "clasificacion": [
            {"p": 1, "n": "BARÇA", "pts": 31},
            {"p": 2, "n": "IGUALADA RIGAT", "pts": 31},
            {"p": 3, "n": "REUS DEPORTIU", "pts": 28}
        ],
        "equipos": [
            {"n": "Barça", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Base"]},
            {"n": "Reus Deportiu Virginias", "reg": "CAT", "ok": True, "cats": ["OK Lliga", "Base"]},
            {"n": "CP Cambrils", "reg": "CAT", "ok": False, "cats": ["2ª Catalana", "Base"]},
            {"n": "Vila-seca CH", "reg": "CAT", "ok": False, "cats": ["2ª Catalana", "Base"]},
            {"n": "Deportivo Liceo", "reg": "ESP", "ok": True, "cats": ["OK Lliga", "Base"]}
            # El robot irá rellenando esto con todos los equipos de las webs
        ]
    }
    with open('hoquei_data.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

update()
