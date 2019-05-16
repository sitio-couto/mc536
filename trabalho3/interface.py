import sqlite3 as sql

def main():
    conn = sql.connect('database.db')
    c = conn.cursor()
    initialize_database(c)

    while(True):
        # Loop trough requests
        request = input()

        # if first char in input isnt a number, read input as a sql query
        if (request.lower() == 'exit'):
            conn.commit()
            conn.close()
            break
        elif request and (not request[0].isdigit()):
            print(request)
            c.execute(request)
            for i in c:
                print(i)
            # print("============================")
        # TODO: Create if-else for eache predefined operation

def initialize_database(c):
    c.execute('CREATE TABLE IF NOT EXISTS Pessoa ( \
                cpf INT NOT NULL, \
                nome VARCHAR(30) NOT NULL,  \
                email VARCHAR(30) NOT NULL, \
                cnpj INT,  \
                PRIMARY KEY (cpf), \
                FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS InstituicaoAcademica ( \
                cnpj INT NOT NULL, \
                nome VARCHAR(30) NOT NULL, \
                PRIMARY KEY (cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Escola ( \
                cnpj INT NOT NULL, \
                nome VARCHAR(30) NOT NULL, \
                posicao_enem INT, \
                PRIMARY KEY (cnpj) \
                FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Universidade ( \
                cnpj INT NOT NULL, \
                nome VARCHAR(30) NOT NULL, \
                ranking INT, \
                PRIMARY KEY (cnpj) \
                FOREIGN KEY (cnpj) REFERENCES InstituicaoAcademica(cnpj) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Questao ( \
                id INT NOT NULL, \
                enunciado VARCHAR(1000) NOT NULL, \
                gabarito VARCHAR(1000) NOT NULL, \
                cpf INT, \
                PRIMARY KEY (id), \
                FOREIGN KEY (cpf) REFERENCES Pessoa(cpf) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Materia ( \
                id INT NOT NULL, \
                nome VARCHAR(30), \
                area_conhecimento VARCHAR(30), \
                PRIMARY KEY (id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Prova ( \
                id INT NOT NULL, \
                nome VARCHAR(30), \
                nivel VARCHAR(30), \
                PRIMARY KEY (id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Realiza ( \
                cpf INT NOT NULL, \
                id_prova INT NOT NULL, \
                n_inscricao INT, \
                PRIMARY KEY (cpf, id_prova), \
                FOREIGN KEY (cpf) REFERENCES Pessoa(cpf), \
                FOREIGN KEY (id_prova) REFERENCES Prova(id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Responde ( \
                cpf INT NOT NULL, \
                id_questao INT NOT NULL, \
                resposta VARCHAR(1000), \
                PRIMARY KEY (cpf, id_questao), \
                FOREIGN KEY (cpf) REFERENCES Pessoa(cpf), \
                FOREIGN KEY (id_questao) REFERENCES Questao(id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Compoe ( \
                id_prova INT NOT NULL, \
                id_questao INT NOT NULL, \
                n_questao INT, \
                PRIMARY KEY (id_prova, id_questao), \
                FOREIGN KEY (id_prova) REFERENCES Prova(id), \
                FOREIGN KEY (id_questao) REFERENCES Questao(id) \
            )')

    c.execute('CREATE TABLE IF NOT EXISTS Aborda ( \
                id_questao INT NOT NULL, \
                id_materia INT NOT NULL, \
                PRIMARY KEY (id_questao, id_materia), \
                FOREIGN KEY (id_questao) REFERENCES Questao(id), \
                FOREIGN KEY (id_materia) REFERENCES Materia(id) \
            )')


### EXECUTION CALL ###
main()
