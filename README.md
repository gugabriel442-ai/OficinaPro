# OficinaPro — Sistema de Gestão de Oficina

Sistema web desenvolvido para facilitar o gerenciamento de uma oficina mecânica, permitindo organizar clientes, veículos e ordens de serviço em uma única aplicação.

## Sobre o projeto

O OficinaPro é um projeto de portfólio desenvolvido para praticar programação back-end, integração com banco de dados e desenvolvimento de interfaces web.

## Funcionalidades

- **Dashboard:** visualização de indicadores de clientes, veículos e ordens de serviço.
- **Clientes:** cadastro, consulta, edição e exclusão.
- **Veículos:** cadastro, consulta, edição e exclusão, com vínculo aos clientes.
- **Ordens de serviço:** cadastro de serviços, descrição e valor.
- **Controle de status:** acompanhamento de serviços pendentes, em andamento e concluídos.
- **Pesquisa e filtros:** busca de ordens por placa, marca, modelo ou descrição e filtragem por status.
- **Exclusão de ordens:** permitida somente para serviços concluídos.
- **Interface responsiva:** layout minimalista para facilitar a utilização.

## Tecnologias utilizadas

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Git e GitHub

## Estrutura do projeto

```text
sistema-oficina/
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── editar_cliente.html
    ├── editar_veiculo.html
    ├── veiculos.html
    └── ordens_servico.html
```

## Como executar o projeto

### 1. Pré-requisitos

- Python instalado
- MySQL instalado
- Git instalado

### 2. Clone o repositório

```bash
git clone https://github.com/gugabriel442-ai/OficinaPro.git
cd OficinaPro
```

### 3. Crie e ative o ambiente virtual

No Windows, usando PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Configure o banco de dados

Crie o banco `oficina_db` no MySQL e configure as tabelas necessárias.

Configure também o arquivo `.env` na raiz do projeto, utilizando as credenciais do seu próprio ambiente:

```dotenv
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=oficina_db
```

Não publique o arquivo `.env` nem suas credenciais no GitHub.

### 6. Execute a aplicação

```bash
python app.py
```

Acesse no navegador o endereço local informado pelo Flask, normalmente:

http://127.0.0.1:5000

## Objetivo de aprendizagem

Este projeto tem como objetivo desenvolver conhecimentos práticos em Python, desenvolvimento web com Flask, operações CRUD, consultas SQL, integração com MySQL e controle de versão com Git e GitHub.

## Autor

Desenvolvido como projeto de portfólio para evolução profissional na área de Tecnologia da Informação.
