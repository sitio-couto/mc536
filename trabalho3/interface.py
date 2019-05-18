from importlib import import_module
from tabulate import tabulate
import sqlite3 as sql

# FUNCTION:
#   main - Process all input from user
# PARAMETERS: 
#   None
# RETUNRS: 
#   None
def main():
    # Connect to database and retrieve cursor
    conn = sql.connect('database.db')
    c = conn.cursor()

    # Loop trough requests until exit case
    while(True):
        # Get input without empty spaces on the beginning
        request = input().strip()

        # Exit the python interface
        if (request.lower() == 'exit'):
            conn.commit() # Write changes to database
            conn.close()  # Close connection to database
            break
        # Initialize and populate database if necessary
        elif (request.lower() == 'setup'):
            # Import tables and random data generator to popuate database
            setup_comands = import_module("database_generator").generate_database()
            # Execute every command
            for sql_command in setup_comands:
                print(sql_command)
                c.execute(sql_command)
            conn.commit() 
        # if first char in input isnt a number, read input as a sql query
        elif request and (not request[0].isdigit()):
            result = c.execute(request)
            print(decorate_table(result))
        # If not empty and is a number (predefined option)
        elif request:
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
                
                result = c.execute(f"SELECT p.cpf \
            	                    FROM Pessoa AS p \
                                    INNER JOIN InstituicaoAcademica AS ia \
                                    ON ia.nome = '{param[1]}' AND ia.cnpj = p.cnpj \
                                    INNER JOIN Realiza AS r \
                                    ON r.id_prova = {param[0]} AND p.cpf = r.cpf;"
                                    )
            # Get all testes from a certain difficulty {param} and above
            elif option=='5':
                # TODO: Since the difficulty is given in strings and there are only two
                # of them (advanced and basic), i considered that the difficulty is related
                # to the alphabetical order of the strings, meaning: Advanced > Basic -> A < B 
                # So if a string comes alphabetically before other, it implies its also
                # more difficult. (Could change to numbers)
                result = c.execute(f"SELECT * \
            	                    FROM Prova \
                                    WHERE Prova.nivel <= '{param}';"
                                    )
            # In case the number is no any of the options, labels as invalid
            else:
                print("Opção inválida!")
                print("=============================================")
                continue

            # Print resulting table in the terminal
            print(decorate_table(result))

        # Print double line to split queries requests
        print("=============================================")

# FUNCTION:
#   decorate_table - formats queries result into table
# PARAMETERS: 
#   result - Iterable object returned by a sqlite3 query
# RETUNRS: 
#   table format compatible with tabulate library
def decorate_table(result):
    # Formatting values 
    values = list(result)
    header = list(map(lambda x: x[0].upper(), list(result.description)))
    # Setting table options
    looks="fancy_grid"
    align="center"
    # Print single line spliting query and table
    print("---------------------------------------------")
    return tabulate(values,headers=header,tablefmt=looks,stralign=align,numalign=align)


### EXECUTION CALL ###
main()
