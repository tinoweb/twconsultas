from flask import Blueprint

# Cria um novo Blueprint para a consulta de placas
placa_bp = Blueprint('placa_bp', __name__)

# Isso importa as rotas definidas em routes.py para este Blueprint
from . import routes
