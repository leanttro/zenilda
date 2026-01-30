import os
import requests
from flask import Flask, render_template, request, jsonify

# Define a pasta onde estão os templates (o index.html)
app = Flask(__name__, template_folder='.')

# --- CONFIGURAÇÃO ---
# Pega a URL do Directus que você configurou no Dokploy
DIRECTUS_URL = os.environ.get("DIRECTUS_URL")

# ROTA 1: A PÁGINA INICIAL
# O Dokploy vai mandar o tráfego de "leanttro.com/zenilda-adv" pra cá.
# Precisamos aceitar tanto com barra no final quanto sem.
@app.route('/zenilda-adv')
@app.route('/zenilda-adv/')
def index():
    return render_template('index.html')

# ROTA 2: O ENDPOINT QUE RECEBE O FORMULÁRIO
# O JavaScript do site vai mandar os dados pra cá.
@app.route('/zenilda-adv/api/cadastro', methods=['POST'])
def cadastro():
    # Validação de segurança básica: Se não tiver URL do Directus, avisa erro.
    if not DIRECTUS_URL:
        print("ERRO: Variável DIRECTUS_URL não encontrada.")
        return jsonify({"erro": "Configuração de servidor incompleta (ENV)"}), 500

    data = request.json
    
    # Prepara o pacote para o Directus
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
        # O timeout evita que o site trave se o Directus demorar
        response = requests.post(DIRECTUS_URL, json=payload, timeout=10)
        
        # Se deu certo (200 OK ou 201 Created)
        if response.status_code in [200, 201]:
            return jsonify({"sucesso": True, "msg": "Lead cadastrado!"}), 200
        else:
            # Se o Directus recusou (Ex: erro de permissão ou campo errado)
            print(f"ERRO DIRECTUS: {response.status_code} - {response.text}")
            return jsonify({"erro": f"Erro no banco de dados: {response.text}"}), 400
            
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        return jsonify({"erro": "Erro interno ao processar envio."}), 500

if __name__ == '__main__':
    # Roda na porta 80 dentro do container
    app.run(host='0.0.0.0', port=80)