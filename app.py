from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    title = ""
    placa = ""

    if request.method == 'POST':
        placa = request.form.get('placa')
        url = f'https://placaconsultar.com.br/Checkouts/{placa}?type=Basica'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            # ... (outros cabeçalhos)
        }

        response = requests.get(url, headers=headers)

        data = {}
        dados = {}

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            info_divs = soup.select("div.row > div > div.form-wrap > ul.list-xxs")

            for div in info_divs:
                label_element = div.find("li", class_="large text-gray-900")
                value_element = div.find("li", class_="heading-5")

                if label_element and value_element:
                    label_text = label_element.text.strip().replace(':', '').replace('/', '_').replace(' ', '_').lower()
                    value_text = value_element.text.strip()
                    data[label_text] = value_text
            
            h3_tag = soup.find('div', class_="col-sm-10 col-lg-8 col-xl-7").find('h3')
            title = h3_tag.text
        
            info_boxes = soup.select("#accordion1-card-body-aoqkylue .info-boxes .form-wrap ul.list-xxs")

            for box in info_boxes:
                label_element = box.find("li", class_="large text-gray-900")
                value_element = box.find("li", class_="heading-5")

                if label_element and value_element:
                    label_text = label_element.text.strip().replace(':', '').replace('/', '_').replace(' ', '_').lower()
                    value_text = value_element.text.strip()
                    dados[label_text] = value_text


        

            # Renomear a chave "placa" para "placa_antiga"
            if "placa" in dados:
                dados["placa_antiga"] = dados.pop("placa")

        # print(json.dumps(dados, indent=4))

    # Fundir os dicionários data e dados
    merged_data = {**data, **dados}

    return render_template('index.html', title=title, **merged_data)

if __name__ == '__main__':
    app.run(debug=True)
