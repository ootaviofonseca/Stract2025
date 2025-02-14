from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

AUTH_TOKEN = 'ProcessoSeletivoStract2025' 
API_BASE_URL = 'https://sidebar.stract.to'

def todos_campos(plataforma):
    campos = [] # Lista de 'field' da plataforma
    camposNomes = [] # Lista de 'name' da plataforma
    pagina = 1 
   
    # O while serve para pegar todos os campos da plataforma, passando por todas as páginas
    while True:
        api_url = f'{API_BASE_URL}/api/fields?platform={plataforma}&page={pagina}'
        response = requests.get(api_url, headers={'Authorization': f'Bearer {AUTH_TOKEN}'})
        if response.status_code == 200:
            data = response.json()
            for field in data.get('fields', []):
                campos.append(field.get('value')) 
                camposNomes.append(field.get('text'))
            
            # Verificar se há mais páginas
            pagination = data.get('pagination', {})
            if pagination.get('current', 1) >= pagination.get('total', 1):
                break  # Se a página atual for maior ou igual ao total, parar o loop
            else:
                pagina += 1  # Caso contrário, incrementar a página para a próxima
        else:
            
            break
            
    return campos, camposNomes

def todos_insights(plataforma, todos_campos):
    dados = {} #dicionario que armazena os insights de cada anuncio de cada conta
    pagina = 1 
    
    # O while serve para pegar todas as contas da plataforma, passando por todas as páginas
    while True:
        api_url = f'{API_BASE_URL}/api/accounts?platform={plataforma}&page={pagina}'
        response = requests.get(api_url, headers={'Authorization': f'Bearer {AUTH_TOKEN}'})
        if response.status_code == 200:
            data = response.json()

            #Esse for pega o 'id' e o 'token' de cada conta por vez
            for account in data.get('accounts', []):
                id = account.get('id') 
                token = account.get('token')
                name = account.get('name')
                
                #Aqui pega todos insights de todos campos da conta
                api_url2 = f'{API_BASE_URL}/api/insights?platform={plataforma}&account={id}&token={token}&fields={",".join(todos_campos)}'
                response2 = requests.get(api_url2, headers={'Authorization': f'Bearer {AUTH_TOKEN}'})
                if response2.status_code == 200:
                    insights = response2.json()

                    # Adiciona o nome da conta a cada insight
                    for insight in insights.get('insights', []):
                        insight['name'] = name  # Adiciona o campo 'name' com o nome da conta

                    # Armazena os insights com o nome da conta no dicionário dados
                    dados[id] = {'insights': insights}
                
                

            # Verificar se há mais páginas
            pagination = data.get('pagination', {})
            if pagination.get('current', 1) >= pagination.get('total', 1):
                break  # Se a página atual for maior ou igual ao total, parar o loop
            else:
                pagina += 1  
        else:
            
            break
    print(dados)
    return dados

def getNomePlataforma(plataforma):
    #/api/platformsj
    api_url = f'{API_BASE_URL}/api/platforms'
    response = requests.get(api_url, headers={'Authorization': f'Bearer {AUTH_TOKEN}'})
    if response.status_code == 200:
        dados = response.json()
        #print(dados)
        for platform in dados.get('platforms', []):
           if platform["value"] == plataforma:    
            return platform["text"]

@app.route("/")
def index ():
    meus_dados = {
        'name': 'Otavio Augusto Trindade Fonseca',
        'email': 'otavioaf123@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/ootaviofonseca'
    }
    return render_template('index.html', **meus_dados)

@app.route("/<plataforma>", methods=['GET'])
def plataforma(plataforma):
    campos, camposNomes = todos_campos(plataforma)
    response = todos_insights(plataforma, campos)
    nomePlataforma=getNomePlataforma(plataforma)
    
    return render_template('plataforma.html',plataforma= nomePlataforma ,camposNomes = camposNomes, dados=response, campos=campos)
    #return jsonify(response)

app.run(debug=True)