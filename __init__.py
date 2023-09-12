from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .consulta_placa import placa
    from .consulta_cpf import cpf
    from .consulta_cnpj import cnpj
    
    app.register_blueprint(placa, url_prefix='/consulta_placa')
    app.register_blueprint(cpf, url_prefix='/consulta_cpf')
    app.register_blueprint(cnpj, url_prefix='/consulta_cnpj')
    
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
