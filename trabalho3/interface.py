from importlib import import_module
import sqlite3 as sql

def main():
    conn = sql.connect('database.db')
    c = conn.cursor()

    while(True):
        # Loop trough requests
        request = input().strip()

        # Exit the python interface
        if (request.lower() == 'exit'):
            conn.commit()
            conn.close()
            break
        # Initialize and populate database if necessary
        elif (request.lower() == 'setup'):
            setup_comands = import_module("database_generator").generate_database()
            for sql_command in setup_comands:
                print(sql_command)
                c.execute(sql_command)
            conn.commit()   # Flush database changes to file
        # if first char in input isnt a number, read input as a sql query
        elif request and (not request[0].isdigit()):
            c.execute(request)
            print("-----------------------------------------")
            for i in c:
                print(i)
        # TODO: Create if-else for eache predefined operation
        # If not empty
        else:
            option = request[0]
            param  = request[2:]

            # Get (cpf,name,email) from every person from {param} academic institution
            if option=='1':
                result = c.execute(f"SELECT p.cpf, p.nome, p.email \
            	                    FROM InstituicaoAcademica AS ia \
                                    INNER JOIN Pessoa AS p \
                                    ON ia.cnpj = p.cnpj \
                                    WHERE ia.nome = '{param}';"
                                    )
            # Get (id) of every question from the subject with id=={param}
            elif option=='2':
                result = c.execute(f"SELECT id_questao \
            	                    FROM Aborda \
                                    WHERE id_materia = {param};"
                                    )
            # Lists the questions descriptions for every question from the test with id=={param}
            elif option=='3':
                result = c.execute(f"SELECT Questao.enunciado \
            	                    FROM Questao INNER JOIN Compoe \
                                    ON Questao.id = Compoe.id_questao \
                                    WHERE Compoe.id_prova = {param};"
                                    )
            # Lists (cpf) from all candidates whom took a test {param[0]} and is part of a certain institution {param[1]}
            elif option=='4':
                param = param.split(' ',1)
                param[1] = param[1].strip()
                print(param)
                result = c.execute(f"SELECT p.cpf \
            	                    FROM Pessoa AS p \
                                    INNER JOIN InstituicaoAcademica AS ia \
                                    ON ia.nome = '{param[1]}' AND ia.cnpj = p.cnpj \
                                    INNER JOIN Realiza AS r \
                                    ON r.id_prova = {param[0]} AND p.cpf = r.cpf;"
                                    )
            # In case the number is no any of the options, labels as invalid
            else:
                print("Opção inválida!")
                print("=============================================")
                continue

            print("-----------------------------------------")
            for tup in result:
                print(tup)
            print("-----------------------------------------")

        print("=============================================")

### EXECUTION CALL ###

main()
