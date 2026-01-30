import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

DIRECTUS_URL = os.environ.get("DIRECTUS_URL")

@app.route('/zenilda-adv')
@app.route('/zenilda-adv/')
def index():
    return render_template('index.html')

@app.route('/zenilda-adv/api/cadastro', methods=['POST'])
def cadastro():
    if not DIRECTUS_URL:
        return jsonify({"erro": "Configuração de servidor incompleta (ENV)"}), 500

    data = request.json
    
    payload = {
        "status": "novo",
        "nome": data.get('nome'),
        "email": data.get('email'),
        "whatsapp": data.get('whatsapp'),
        "area_atuacao": data.get('area_atuacao'),
        "origem": "landing_zenilda_advogados"
    }

    try:
        response = requests.post(DIRECTUS_URL, json=payload, timeout=10)
        
        # CORREÇÃO AQUI: Adicionei o 204 na lista de sucessos
        if response.status_code in [200, 201, 204]:
            return jsonify({"sucesso": True, "msg": "Lead cadastrado!"}), 200
        else:
            print(f"ERRO DIRECTUS: {response.status_code} - {response.text}")
            return jsonify({"erro": f"Erro no banco de dados: {response.text}"}), 400
            
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        return jsonify({"erro": "Erro interno ao processar envio."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)