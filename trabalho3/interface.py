from importlib import import_module
from tabulate import tabulate
import sqlite3 as sql
import optparse

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

    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', dest='show_params', action='store_true')
    show_params = parser.parse_args()[0].show_params # True if '-v' is used and None otherwise

    show_options(show_params)

    # Loop trough requests until exit case
    while(True):
        # Get input without empty spaces on the beginning
        request = input().strip()

        # Exit the python interface
        if (request.lower() in ['exit', 'quit', 'q', 'sair']):
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
        # Count all records in the database (size etimate)
        elif (request.lower() == 'size'):
            show_database_size(c)
        # if first char in input isnt a number, read input as a sql query
        elif request and (not request[0].isdigit()):
            try: 
                result = c.execute(request)
                if result.description: # Checks if there's a resulting table to print
                    print(decorate_table(result))
            except: 
                print("---------------------------------------------")
                print("Query inválida! Corrigir sintaxe.")
        # If not empty and is a number (predefined option)
        elif request:
            request = request.split(" ",1)
            option = request.pop(0)
            if request: param = request[0]
            else: param = ""

            # Get (cpf,name,email) from every person from {param} academic institution
            if option=='1' and param:
                result = c.execute(f"SELECT p.cpf, p.nome, p.email \
            	                    FROM InstituicaoAcademica AS ia \
                                    INNER JOIN Pessoa AS p \
                                    ON ia.cnpj = p.cnpj \
                                    WHERE ia.nome = '{param}';"
                                    )
            # Get (id) of every question from the subject with id=={param}
            elif option=='2' and param:
                result = c.execute(f"SELECT id_questao \
            	                    FROM Aborda \
                                    WHERE id_materia = {param};"
                                    )
            # Lists the questions descriptions for every question from the test with id=={param}
            elif option=='3' and param:
                result = c.execute(f"SELECT Questao.enunciado \
            	                    FROM Questao INNER JOIN Compoe \
                                    ON Questao.id = Compoe.id_questao \
                                    WHERE Compoe.id_prova = {param};"
                                    )
            # Lists (cpf) from all candidates whom took a test {param[0]} and is part of a certain institution {param[1]}
            elif option=='4' and param:
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
            elif option=='5' and param:
                # TODO: The option should list all difficulties equal or 
                # superior to PARAM. Since the difficulty is given in strgins,
                # i changed the query to select onlt difficulties from PARAM level.
                result = c.execute(f"SELECT * \
            	                    FROM Prova \
                                    WHERE Prova.nivel >= '{param}';"
                                    )
            # In case the number is no any of the options, labels as invalid
            else:
                if option not in '1,2,3,4,5':
                    print("Opção inválida!")
                elif not param:
                    print("Falta argumentos para a opção desejada.")    
                else:
                    print("Erro desconhecido.")

                print("=============================================")
                continue
            
            # Print resulting table in the terminal
            print(decorate_table(result))

        # Print double line to split queries requests
        print("=============================================")
        show_options(show_params)

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

# FUNCTION:
#   show_database_size - calculates total of entries for each table and its sum
# PARAMETERS: 
#   c - SQLite3 cursor object use to access database info
def show_database_size(c):
    print("----------------------------")
    count = 0
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    for i in list(c.execute(query)):
        for qnt in c.execute(f"SELECT COUNT(*) FROM {i[0]};"):
            count += qnt[0]
            print(i[0], "possui", qnt[0], "registros.")
    print("----------------------------")
    print(f"TOTAL DE REGISTROS: {count}")
    return

def show_options(show_params=False):
    options = [ "1 - Listar alunos (CPF, nome, email) de uma Instituição Acadêmica",
                "2 - Listar IDs das questões de uma matéria",
                "3 - Listar questões de uma prova",
                "4 - Listar CPFs dos candidatos que fizeram uma prova e pertencem a uma Instituição Acadêmica",
                "5 - Listar provas dado um nível de dificuldade",
                "Escolha uma das opções acima ou digite uma query SQL:",
                "---------------------------------------------"
              ]
    if show_params:
        options[0] += "\n    1 <nome da  instituição>"
        options[1] += "\n    2 <id da matéria>"
        options[2] += "\n    3 <id da prova>"
        options[3] += "\n    4 <id da prova> <nome da  instituição>"
        options[4] += "\n    5 <nível  de  dificuldade>"
    for i in options : print(i)
    return

### EXECUTION CALL ###
main()
