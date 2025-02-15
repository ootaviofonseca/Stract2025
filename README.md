

# API de Relatórios - Stract

Este projeto é uma API desenvolvida para consumir dados de uma API externa e gerar relatórios em tempo real. O servidor é escrito em Python utilizando Flask e possui endpoints que processam e exibem os dados em relatórios conforme solicitado.

## Como instalar

### 1. Clone o repositório
Primeiro, faça o clone deste repositório para o seu computador:
```bash
git clone https://github.com/ootaviofonseca/Stract2025.git
cd Stract2025
```

### 2. Crie um ambiente virtual
Recomenda-se criar um ambiente virtual para o projeto:
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
- No Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Instale as dependências
Com o ambiente virtual ativado, instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

### 5. Rodar o servidor
Para iniciar o servidor Flask, execute:
```bash
python app.py
```

O servidor estará disponível em `http://localhost:5000`.

## Endpoints

A API possui os seguintes endpoints:

### `/`
Retorna minhas informacoes pessoais

### `/{{plataforma}}`
Retorna uma tabela com todos os anúncios veiculados na plataforma indicada. As colunas contêm os campos de insights dos anúncios, além do nome da conta que está veiculando o anúncio.

**Exemplo de resposta:**
```csv
Platforma,Ad Name,Clicks,...
Facebook,Some Ad,10,...
Facebook,Other Ad,20,...
YouTube,One More Ad,5,...
```

### `/{{plataforma}}/resumo`
Retorna uma tabela similar ao endpoint anterior, mas agregando os dados por conta. As colunas numéricas são somadas e as colunas de texto ficam vazias (exceto o nome da conta).

**Exemplo de resposta:**
```csv
Platform,Ad Name,Clicks,...
Facebook,,30,...
YouTube,,5,...
```

### `/geral`
Retorna todos os anúncios de todas as plataformas, com a coluna adicional indicando a plataforma e o nome da conta. Todos os campos da API são incluídos.

**Exemplo de resposta:**
```csv
Platform,Ad Name,Clicks,...,Platform Name,Account Name
Facebook,Some Ad,10,...,Facebook,Account1
Facebook,Other Ad,20,...,Facebook,Account2
YouTube,One More Ad,5,...,YouTube,Account3
```

### `/geral/resumo`
Retorna uma tabela agregada por plataforma. Os dados numéricos são somados e as colunas de texto ficam vazias (exceto o nome da plataforma).

**Exemplo de resposta:**
```csv
Platform,Ad Name,Clicks,...
Facebook,,50,...
YouTube,,5,...
```

## Exemplo de uso

1. Para acessar a lista de plataformas disponíveis:
   ```bash
   curl http://localhost:5000/api/platforms
   ```

2. Para acessar os anúncios de uma plataforma específica, como "Facebook":
   ```bash
   curl http://localhost:5000/facebook
   ```

3. Para acessar o resumo dos anúncios de uma plataforma específica:
   ```bash
   curl http://localhost:5000/facebook/resumo
   ```

4. Para acessar os relatórios gerais:
   ```bash
   curl http://localhost:5000/geral
   ```

5. Para acessar o resumo geral:
   ```bash
   curl http://localhost:5000/geral/resumo
   ```

## Tecnologias utilizadas

- **Flask**: Framework web para Python.
- **Requests**: Para fazer requisições à API externa de dados de anúncios.

## Considerações

Este projeto foi desenvolvido para o processo seletivo da Stract e segue as especificações solicitadas no enunciado do desafio.


