import sqlite3 as sql

def main():
    conn = sql.connect('database.db')
    c = conn.cursor()
    initialize_database(c)

    while(True):
        # Loop trough requests
        # c.execute("INSERT INTO pessoa VALUES (00000000000,'Sitio','sitio@unicamp.br',NULL)")
        conn.commit()
        for i in c.execute("SELECT * FROM Pessoa"):
            print(i)
        break

    conn.close()

def initialize_database(c):
    c.execute('CREATE TABLE IF NOT EXISTS Pessoa ( \
                cpf INT, \
                nome VARCHAR(30) NOT NULL,  \
                email VARCHAR(30) NOT NULL, \
                cnpj INT,  \
                PRIMARY KEY (cpf) \
                FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS InstituicaoAcademica ( \
                cnpj INT, \
                nome VARCHAR(30) NOT NULL, \
                PRIMARY KEY (cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Escola ( \
                cnpj INT, \
                nome VARCHAR(30) NOT NULL, \
                posicao_enem INT, \
                PRIMARY KEY (cnpj) \
                FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Universidade ( \
                cnpj INT, \
                nome VARCHAR(30) NOT NULL, \
                ranking INT, \
                PRIMARY KEY (cnpj) \
                FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Questao ( \
                id INT, \
                enunciado VARCHAR(1000) NOT NULL, \
                gabarito VARCHAR(1000) NOT NULL, \
                cpf INT, \
                PRIMARY KEY (id), \
                FOREIGN KEY (cpf) REFERENCES Pessoa(cpf) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Materia ( \
                id INT, \
                nome VARCHAR(30), \
                area_conhecimento VARCHAR(30), \
                PRIMARY KEY (id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Prova ( \
                id INT, \
                nome VARCHAR(30), \
                nivel VARCHAR(30), \
                PRIMARY KEY (id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Realiza ( \
                cpf INT, \
                id_prova INT, \
                n_inscricao INT, \
                PRIMARY KEY (cpf, id_prova), \
                FOREIGN KEY (cpf) REFERENCES Pessoa(cpf), \
                FOREIGN KEY (id_prova) REFERENCES Prova(id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Responde ( \
                cpf INT, \
                id_questao INT, \
                resposta VARCHAR(1000), \
                PRIMARY KEY (cpf, id_questao), \
                FOREIGN KEY (cpf) REFERENCES Pessoa(cpf), \
                FOREIGN KEY (id_questao) REFERENCES Questao(id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Compoe ( \
                id_prova INT, \
                id_questao INT, \
                n_questao INT, \
                PRIMARY KEY (id_prova, id_questao), \
                FOREIGN KEY (id_prova) REFERENCES Prova(id), \
                FOREIGN KEY (id_questao) REFERENCES Questao(id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Aborda ( \
                id_questao INT, \
                id_materia INT, \
                PRIMARY KEY (id_questao, id_materia), \
                FOREIGN KEY (id_questao) REFERENCES Questao(id), \
                FOREIGN KEY (id_materia) REFERENCES Materia(id) \
            )')


### EXECUTION CALL ###
main()