from importlib import import_module
import sqlite3 as sql

def main():
    conn = sql.connect('database.db')
    c = conn.cursor()

    while(True):
        # Loop trough requests
        request = input()

        # if first char in input isnt a number, read input as a sql query
        if (request.lower() == 'exit'):
            conn.commit()
            conn.close()
            break
        elif (request.lower() == 'setup'):
            setup_comands = import_module("database_generator").generate_database()
            for sql_command in setup_comands:
                print(sql_command)
                c.execute(sql_command)
            conn.commit()   # Flush database changes to file
        elif request and (not request[0].isdigit()):
            c.execute(request)
            print("-----------------------------------------")
            for i in c:
                print(i)
            print("-----------------------------------------")
        # TODO: Create if-else for eache predefined operation

        print("=============================================")

### EXECUTION CALL ###

main()
