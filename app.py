from collections import defaultdict
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

def resumo_todos_insights( todosDados, camposNomes):
    agrupadoNomes = {}
    grupoFinal = {}
    for key, value in todosDados.items():
        insights = value.get('insights', {}).get('insights', [])
        for insight in insights:
            # Usamos o campo 'name' para agrupar os objetos
            nome = insight.get('name')
            if nome in agrupadoNomes:
                agrupadoNomes[nome].append(insight)
            else:
                agrupadoNomes[nome] = [insight]
    
    for name, value in agrupadoNomes.items():
        if name not in grupoFinal:
            grupoFinal[name] = {campo: None for campo in camposNomes}
        for insight in value:
                for campo in camposNomes:
                    campo_valor = insight.get(campo)
                    if campo_valor is not None:
                        if isinstance(campo_valor, (int, float)):
                            if grupoFinal[name][campo] is None:
                                grupoFinal[name][campo] = 0  
                            if name in grupoFinal:
                                grupoFinal[name][campo] += insight[campo]
                                grupoFinal[name][campo] = round(grupoFinal[name][campo], 3)



    print(grupoFinal)
    # Converter de volta para um dicionário regular, se necessário
    return grupoFinal

def getGeral():
    #Essa funcao pega todos os dados de todas as plataformas
    todasPlataformas = []
    nomesPlataforma = []
    todosCampos = []
    todosCamposNomes = []
    agrupados = {} #serve para agrupar as referencias de cada chave e nome de campo de cada plataforma
    geral_dados = {}
    
    api_url = f'{API_BASE_URL}/api/platforms'
    response = requests.get(api_url, headers={'Authorization': f'Bearer {AUTH_TOKEN}'})
    if response.status_code == 200:
        dados = response.json()
        for platform in dados.get('platforms', []):
            plataforma = platform["value"]
            nomePlataforma = platform["text"]
            nomesPlataforma.append(nomePlataforma)
            campos, camposNomes = todos_campos(plataforma)
            todosCampos.extend(campos)
            todosCamposNomes.extend(camposNomes)
            todasPlataformas.append(plataforma) 
            geral_dados[plataforma] = todos_insights(plataforma, todosCampos)
     
    for i, nome in enumerate(todosCamposNomes):
        if nome not in agrupados:
            agrupados[nome] = []  # Inicializa uma lista para os campos correspondentes
        agrupados[nome].append(todosCampos[i])  # Agrupa os valores de todosCampos

    
    return geral_dados, agrupados, nomesPlataforma

def resumoPorPlataforma(plataforma):
    resumo = {}

    campos, camposNomes = todos_campos(plataforma)
    response = todos_insights(plataforma, campos)

    for key, value in response.items():
        insights = value.get('insights', {}).get('insights', [])
        for insight in insights:
            
            for campo, valor in insight.items():
                if isinstance(valor, (int, float)):
                    if campo not in resumo:
                        resumo[campo] = 0  
                    resumo[campo] = round(resumo[campo] + valor, 3)
                else:
                    resumo[campo] = '-'    
 
    return resumo, camposNomes, campos
    
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

@app.route("/<plataforma>/resumo", methods=['GET'])
def platafroamResumo(plataforma):
    nomePlataforma=getNomePlataforma(plataforma)
    campos, camposNomes = todos_campos(plataforma)
    response = todos_insights(plataforma, campos)
    resumo = resumo_todos_insights(response, campos)
    
    return render_template('plataforma_resumo.html', plataforma= nomePlataforma ,camposNomes = camposNomes, dados=resumo, campos=campos)

@app.route("/geral", methods=['GET'])
def geral():
    geral_dados, agrupados, nomesPlataforma = getGeral()
    
    # Agora você tem todos os dados no formato necessário. Exibindo-os em uma página HTML ou retornando como JSON:
    return render_template('geral.html', dados=geral_dados, agrupados=agrupados, nomesPlataforma=nomesPlataforma)

@app.route("/geral/resumo", methods=['GET'])
def geralResumo():
    resumos = {}
    agrupados = {}
    api_url = f'{API_BASE_URL}/api/platforms'
    response = requests.get(api_url, headers={'Authorization': f'Bearer {AUTH_TOKEN}'})
    if response.status_code == 200:
        dados = response.json()
        for platform in dados.get('platforms', []):
            plataforma = platform["value"]
            nome = platform['text']
            resumo, camposNomes, campos  = resumoPorPlataforma(plataforma)
            for campo in camposNomes:
                if campo not in agrupados:
                    agrupados[campo] = []
                agrupados[campo].append(campos[camposNomes.index(campo)])
            resumos[nome] = resumo
    
    
    
    return render_template('geral_resumo.html', dados=resumos, agrupados=agrupados)

app.run(debug=True)