
CREATE TABLE Pessoa (
    cpf INT NOT NULL, 
    nome VARCHAR(30) NOT NULL,  
    email VARCHAR(30) NOT NULL, 
    cnpj INT,  
    PRIMARY KEY (cpf), 
    FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) 
);

CREATE TABLE InstituicaoAcademica ( 
    cnpj INT NOT NULL, 
    nome VARCHAR(30) NOT NULL, 
    PRIMARY KEY (cnpj) 
);

CREATE TABLE Escola ( 
    cnpj INT NOT NULL, 
    nome VARCHAR(30) NOT NULL, 
    posicao_enem INT, 
    PRIMARY KEY (cnpj),
    FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) 
);

CREATE TABLE Universidade ( 
    cnpj INT NOT NULL, 
    nome VARCHAR(30) NOT NULL, 
    ranking INT, 
    PRIMARY KEY (cnpj),
    FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) 
);

CREATE TABLE Questao ( 
    id INT NOT NULL, 
    enunciado VARCHAR(1000) NOT NULL, 
    gabarito VARCHAR(1000) NOT NULL, 
    cpf INT, 
    PRIMARY KEY (id), 
    FOREIGN KEY (cpf) REFERENCES Pessoa(cpf) 
);

CREATE TABLE Materia ( 
    id INT NOT NULL, 
    nome VARCHAR(30), 
    area_conhecimento VARCHAR(30), 
    PRIMARY KEY (id) 
);

CREATE TABLE Prova ( 
    id INT NOT NULL, 
    nome VARCHAR(30), 
    nivel VARCHAR(30), 
    PRIMARY KEY (id) 
);

CREATE TABLE Realiza ( 
    cpf INT NOT NULL, 
    id_prova INT NOT NULL, 
    n_inscricao INT, 
    PRIMARY KEY (cpf, id_prova), 
    FOREIGN KEY (cpf) REFERENCES Pessoa(cpf), 
    FOREIGN KEY (id_prova) REFERENCES Prova(id) 
);

CREATE TABLE Responde ( 
    cpf INT NOT NULL, 
    id_questao INT NOT NULL, 
    resposta VARCHAR(1000), 
    PRIMARY KEY (cpf, id_questao), 
    FOREIGN KEY (cpf) REFERENCES Pessoa(cpf), 
    FOREIGN KEY (id_questao) REFERENCES Questao(id) 
);

CREATE TABLE Compoe ( 
    id_prova INT NOT NULL, 
    id_questao INT NOT NULL, 
    n_questao INT, 
    PRIMARY KEY (id_prova, id_questao), 
    FOREIGN KEY (id_prova) REFERENCES Prova(id), 
    FOREIGN KEY (id_questao) REFERENCES Questao(id) 
);

CREATE TABLE Aborda ( 
    id_questao INT NOT NULL, 
    id_materia INT NOT NULL, 
    PRIMARY KEY (id_questao, id_materia), 
    FOREIGN KEY (id_questao) REFERENCES Questao(id), 
    FOREIGN KEY (id_materia) REFERENCES Materia(id) 
);