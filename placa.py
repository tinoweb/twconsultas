from flask import Flask, render_template
from consulta_placa.routes import placa_bp
from consulta_cpf.routes import cpf_bp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Registra o Blueprint
app.register_blueprint(placa_bp)
app.register_blueprint(cpf_bp)

if __name__ == '__main__':
    app.run(debug=True)