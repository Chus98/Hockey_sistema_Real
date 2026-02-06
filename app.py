from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    datos = {
        "ciudad": "Reus, Cataluña",
        "temperatura": "19°C",
        "clasificacion": [
            { "p": 1, "n": "HOCKEY CLUB LICEO", "pts": 45 },
            { "p": 2, "n": "BARÇA", "pts": 42 },
            { "p": 3, "n": "IGUALADA RIGAT HC", "pts": 39 },
            { "p": 4, "n": "CALAFELL LA MENDOCINA", "pts": 35 },
            { "p": 5, "n": "REUS DEPORTIU VIRGINIAS", "pts": 30 }
        ]
    }
    return render_template('index.html', **datos)

if __name__ == '__main__':
    app.run(debug=True)
