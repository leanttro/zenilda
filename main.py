import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

# --- CONFIGURAÇÃO ---
# No Dokploy, adicione a variável: DIRECTUS_URL
# Exemplo de valor: https://admin.leanttro.com/items/leads_adv
DIRECTUS_URL = os.environ.get("DIRECTUS_URL")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    if not DIRECTUS_URL:
        return jsonify({"erro": "URL do Directus não configurada no Dokploy"}), 500

    data = request.json
    
    # Força a origem para garantir que veio daqui
    payload = {
        "status": "novo",
        "nome": data.get('nome'),
        "email": data.get('email'),
        "whatsapp": data.get('whatsapp'),
        "area_atuacao": data.get('area_atuacao'),
        "origem": "landing_zenilda_advogados"
    }

    try:
        # Envia para o Directus
        response = requests.post(DIRECTUS_URL, json=payload)
        
        if response.status_code in [200, 201]:
            return jsonify({"sucesso": True, "msg": "Lead cadastrado!"}), 200
        else:
            return jsonify({"erro": f"Erro Directus: {response.text}"}), 400
            
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)