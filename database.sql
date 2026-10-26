
-- =========================================
-- OficinaPro - Banco de dados
-- =========================================

CREATE DATABASE IF NOT EXISTS oficina_db;

USE oficina_db;

-- =========================================
-- TABELA DE CLIENTES
-- =========================================

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- TABELA DE VEÍCULOS
-- =========================================

CREATE TABLE IF NOT EXISTS veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    ano INT NOT NULL,
    placa VARCHAR(10) NOT NULL UNIQUE,

    CONSTRAINT fk_veiculos_clientes
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
);

-- =========================================
-- TABELA DE ORDENS DE SERVIÇO
-- =========================================

CREATE TABLE IF NOT EXISTS ordens_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    veiculo_id INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Pendente',
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ordens_veiculos
        FOREIGN KEY (veiculo_id)
        REFERENCES veiculos(id)
);
