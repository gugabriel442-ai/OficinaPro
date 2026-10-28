# OficinaPro — Sistema de Gestão para Oficinas Mecânicas

O **OficinaPro** é uma aplicação web desenvolvida para facilitar o gerenciamento de oficinas mecânicas. O sistema permite administrar clientes, veículos e ordens de serviço por meio de uma interface web simples e intuitiva.

## 🌐 Aplicação online

**Acesse o sistema:** https://oficinapro-nwi1.onrender.com

## ✨ Funcionalidades

- Cadastro e gerenciamento de clientes.
- Consulta, edição e exclusão de clientes.
- Cadastro e gerenciamento de veículos.
- Edição e exclusão de veículos.
- Criação e gerenciamento de ordens de serviço.
- Atualização do status das ordens de serviço.
- Pesquisa e filtros para localizar registros.
- Visualização dos detalhes das ordens de serviço.
- Integração com banco de dados MySQL.

## 🛠️ Tecnologias utilizadas

- **Python** — lógica e processamento da aplicação.
- **Flask** — framework para desenvolvimento web.
- **MySQL** — banco de dados relacional.
- **HTML** — estrutura das páginas.
- **CSS** — estilização da interface.
- **Git e GitHub** — versionamento e gerenciamento do código-fonte.
- **Render** — hospedagem da aplicação web.
- **Aiven** — hospedagem do banco de dados MySQL.

## 📂 Estrutura do projeto

```text
sistema-oficina/
├── certificados/
│   └── ca.pem
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

**Observação:** os diretórios `.venv` e `__pycache__` foram omitidos da estrutura acima porque são arquivos locais de ambiente e execução.

## ⚙️ Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/gugabriel442-ai/OficinaPro.git
cd OficinaPro
```

### 2. Criar um ambiente virtual

```bash
python -m venv .venv
```

No Windows PowerShell, ative-o com:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as configurações do banco de dados:

```env
DB_HOST=seu_host
DB_PORT=sua_porta
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
```

Substitua os valores pelos dados da sua instância MySQL. Não publique o arquivo `.env` nem compartilhe suas credenciais.

### 5. Preparar o banco de dados

Execute o script `database.sql` em uma instância MySQL compatível, verificando previamente o nome do banco de dados utilizado.

### 6. Executar a aplicação

```bash
python app.py
```

Acesse o endereço local indicado pelo Flask no terminal.

## ☁️ Hospedagem

A aplicação está publicada no Render e utiliza um banco de dados MySQL hospedado no Aiven.

- **Aplicação:** https://oficinapro-nwi1.onrender.com
- **Código-fonte:** https://github.com/gugabriel442-ai/OficinaPro

As credenciais e configurações de produção são definidas por variáveis de ambiente no serviço de hospedagem.

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido para praticar e consolidar conhecimentos em programação Python, desenvolvimento web com Flask, integração com bancos de dados relacionais, versionamento com Git e GitHub e publicação de aplicações na nuvem.

## 👨‍💻 Autor

GitHub: [gugabriel442-ai](https://github.com/gugabriel442-ai)