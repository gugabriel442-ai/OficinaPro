# OficinaPro — Sistema de Gestão de Oficina

Sistema web para gerenciamento de oficinas mecânicas, desenvolvido com Python, Flask e MySQL. O projeto permite organizar clientes, veículos e ordens de serviço em uma interface simples e minimalista.

## Sobre o projeto

O OficinaPro é um projeto de portfólio criado para praticar desenvolvimento web, programação back-end, integração com banco de dados relacionais e controle de versão com Git e GitHub.

## Funcionalidades

### Dashboard
- Visualização de indicadores de clientes, veículos e ordens de serviço.
- Atalhos para acessar as principais áreas do sistema.
- Listagem e pesquisa de clientes.

### Clientes
- Cadastro de clientes.
- Consulta e pesquisa por nome, telefone ou e-mail.
- Edição e exclusão de registros.
- Proteção contra exclusão de clientes que possuem veículos cadastrados.

### Veículos
- Cadastro de veículos vinculados a clientes.
- Consulta e pesquisa por placa, marca ou modelo.
- Edição e exclusão de registros.
- Proteção contra exclusão de veículos vinculados a ordens de serviço.

### Ordens de serviço
- Cadastro de ordens com veículo, descrição e valor.
- Consulta dos dados do cliente e do veículo relacionado.
- Pesquisa por nome do cliente, placa, marca, modelo ou descrição do serviço.
- Filtro por status.
- Atualização do status: Pendente, Em andamento ou Concluída.
- Página com detalhes completos da ordem de serviço.
- Exclusão permitida somente para ordens concluídas.

## Tecnologias utilizadas

- **Python:** lógica e processamento da aplicação.
- **Flask:** desenvolvimento da aplicação web.
- **MySQL:** armazenamento e gerenciamento dos dados.
- **HTML5:** estrutura das páginas.
- **CSS3:** estilização e responsividade.
- **Git:** controle de versão.
- **GitHub:** hospedagem do código-fonte.

## Estrutura do projeto

```text
sistema-oficina/
├── static/
│   └── style.css
├── templates/
│   ├── detalhes_ordem.html
│   ├── editar_cliente.html
│   ├── editar_veiculo.html
│   ├── index.html
│   ├── ordens_servico.html
│   └── veiculos.html
├── .env
├── .gitignore
├── app.py
├── database.py
├── database.sql
├── README.md
└── requirements.txt
```

O ambiente virtual `.venv/` e a pasta `__pycache__/` são locais e não precisam ser publicados no repositório.

## Como executar o projeto

### 1. Pré-requisitos

Antes de começar, instale:

- Python 3.
- MySQL Server.
- MySQL Workbench (opcional, recomendado para administrar o banco).
- Git.

### 2. Clonar o repositório

```bash
git clone https://github.com/gugabriel442-ai/OficinaPro.git
cd OficinaPro
```

### 3. Criar o ambiente virtual

No Windows, utilizando PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install -r requirements.txt
```

### 5. Configurar o banco de dados

Abra o MySQL Workbench, conecte-se ao seu servidor MySQL e execute o conteúdo do arquivo `database.sql`.

O script cria o banco de dados e as tabelas necessárias para o funcionamento do sistema.

### 6. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, no mesmo nível de `app.py` e `database.py`.

Configure as credenciais do seu próprio ambiente:

```env
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=oficina_db
```

Substitua `seu_usuario` e `sua_senha` pelas credenciais válidas do MySQL.

**Importante:** nunca publique o arquivo `.env` nem compartilhe suas credenciais. O arquivo deve estar listado no `.gitignore`.

### 7. Executar a aplicação

No terminal, com o ambiente virtual ativado, execute:

```bash
python app.py
```

Abra o navegador no endereço:

http://127.0.0.1:5000

## Segurança e boas práticas

- Credenciais do banco de dados armazenadas em variáveis de ambiente.
- Consultas SQL parametrizadas para operações com dados fornecidos pelo usuário.
- Uso de Git para acompanhar alterações no código.
- Arquivos locais e credenciais excluídos do versionamento por meio do `.gitignore`.

## Objetivo de aprendizagem

O projeto tem como objetivo desenvolver conhecimentos práticos em Python, Flask, operações CRUD, consultas SQL, integração com MySQL, desenvolvimento de interfaces web e controle de versão com Git e GitHub.

## Autor

Projeto desenvolvido para portfólio profissional e evolução na área de Tecnologia da Informação.
