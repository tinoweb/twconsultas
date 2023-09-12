from flask import Blueprint, render_template, request
from .consulta import funcao_que_consulta_placa
from pprint import pprint  # <-- Importe a função


placa_bp = Blueprint('placa', __name__, template_folder='templates')

@placa_bp.route('/consulta_placa', methods=['GET', 'POST'])
def consulta_placa():
    resultado = {}
    if request.method == 'POST':
        placa_digitada = request.form.get('placa')  # use .get() para evitar KeyErrors
        if placa_digitada:  # verifique se a placa foi realmente fornecida
            resultado = funcao_que_consulta_placa(placa_digitada)
            pprint(resultado)  # <-- Imprima o resultado aqui

    return render_template('consulta_placa.html', **resultado)
