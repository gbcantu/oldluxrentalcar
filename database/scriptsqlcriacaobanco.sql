CREATE TABLE Cliente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(15)
);

CREATE TABLE Veiculo (
    id SERIAL PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    ano_fabricacao DATE NOT NULL ,
    placa VARCHAR(10) UNIQUE NOT NULL,
    valor_diaria NUMERIC(10,2) NOT NULL ,
    quilometragem_atual INTEGER NOT NULL ,
    disponivel BOOLEAN NOT NULL
);

CREATE TABLE Agendamento (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES Cliente(id),
    veiculo_id INTEGER NOT NULL REFERENCES Veiculo(id),
    data_inicio DATE NOT NULL ,
    data_fim DATE NOT NULL ,
    valor_total NUMERIC(10,2) NOT NULL ,
    quilometragem_retirada INTEGER NOT NULL,
    quilometragem_devolucao INTEGER NOT NULL ,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE Manutencao (
    id SERIAL PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES Veiculo(id),
    tipo VARCHAR(50) NOT NULL,
    data DATE NOT NULL,
    descricao TEXT,
    custo NUMERIC(10,2) NOT NULL ,
    quilometragem INTEGER NULL 
);

CREATE TABLE DocumentoVeiculo (
    id SERIAL PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES Veiculo(id),
    tipo_documento VARCHAR(50) NOT NULL,
    numero_documento VARCHAR(50) NOT NULL,
    validade_inicio DATE NOT NULL,
    validade_fim DATE NOT NULL ,
    observacoes TEXT
);

