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
            print("-----------------------------------------")
        # TODO: Create if-else for eache predefined operation
        # If not empty
        else:
            option = request[0]
            param  = request[2:]

            if option=='1':
                result = c.execute(f"SELECT p.nome \
            	                    FROM InstituicaoAcademica AS ia\
                                    INNER JOIN Pessoa AS p \
                                    ON ia.nome = '{param}' AND ia.cnpj = p.cnpj;"
                                    )
            # elif option=='2':
                
            # elif option=='3':
            
            # elif option=='4':
            
            else:
                print("Opção inválida!")
                print("=============================================")
                continue

            for tup in result:
                print(tup)
                

        print("=============================================")

### EXECUTION CALL ###

main()
