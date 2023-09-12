from flask import Blueprint, render_template, request, flash, jsonify

import requests
from bs4 import BeautifulSoup
from datetime import datetime

cpf_bp = Blueprint('consulta_cpf', __name__, template_folder='templates')

@cpf_bp.route('/consulta_cpf', methods=['GET'])
def mostrar_formulario():
    resultado = {}  # Inicializa a variável resultado como um dicionário vazio
    return render_template('consulta_cpf.html', resultado=resultado)

@cpf_bp.route('/scrape', methods=['POST'])
def consulta_cpf():
     # Obtenha os dados do formulário
    cpf = request.form.get('cpf')
    birthdate = request.form.get('birthdate')

    # Remova todos os pontos e traços do CPF
    cpf = cpf.replace(".", "").replace("-", "")

    print(cpf)
    print(birthdate)

    # Lógica de consulta aqui (adaptada ao Blueprint)
    api_url = f'https://api.nfse.io/NaturalPeople/Basicinfo/taxNumber/{cpf}/{birthdate}'
    
    try:
        # Realize a solicitação HTTP para a API
        response = requests.get(api_url)
        response.raise_for_status()  # Verifique se a solicitação foi bem-sucedida

        # Simule a extração de dados do JSON da API (substitua com a lógica real)
        data = response.json()

        # Extraia os campos do JSON
        natural_person = data.get('naturalPerson', {})

        # Formate as datas no formato "dia/mês/ano"
        birthOn = natural_person.get('birthOn', 'Data de nascimento não encontrada')
        if birthOn != 'Data de nascimento não encontrada':
            birthOn = datetime.fromisoformat(birthOn).strftime('%d/%m/%Y')
        
        createdOn = natural_person.get('createdOn', 'Data de criação não encontrada')
        if createdOn != 'Data de criação não encontrada':
            createdOn = datetime.fromisoformat(createdOn).strftime('%d/%m/%Y')

        # Retorne os dados em um formato JSON
        resultado_consulta = {
            'createdOn': createdOn,
            'birthOn': birthOn,
            'status': natural_person.get('status', 'Status não encontrado'),
            'name': natural_person.get('name', 'Nome não encontrado'),
            'federalTaxNumber': natural_person.get('federalTaxNumber', 'CPF não encontrado')
        }

        return render_template('consulta_cpf.html', resultado=resultado_consulta)

    except requests.exceptions.RequestException as e:
        # Em caso de falha na solicitação, retorne uma mensagem de erro em formato JSON
        resultado_erro = {'error': "Consulta não Encontrada - CPF e Data de Nascimento Não Encontrada."}
        return render_template('consulta_cpf.html', resultado=resultado_erro)