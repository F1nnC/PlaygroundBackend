import sqlite3

database= 'projects/sqlite.db'

import os

if not os.path.exists('projects'):
    os.makedirs('projects')

def schema():
    #Connecting to sqliter
    conn = sqlite3.connect(database)

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # CREATE
    #Doping PLAYERS table if already exists.
    cursor.execute("DROP TABLE IF EXISTS PLAYERS")

    #Creating table as per requirement
    sql ='''CREATE TABLE PLAYERS(
    USER_NAME CHAR(20) NOT NULL,
    UID INT,
    PASSWORD CHAR(20),
    SCORE INT
    )'''
    cursor.execute(sql)
    #"Table created successfully........"

    # Preparing SQL queries to INSERT a record into the database.
    cursor.execute('''INSERT INTO PLAYERS(
    USER_NAME, UID, PASSWORD, SCORE) VALUES 
    ('Ramya', '17898', ' 4567898', '10')''')
    cursor.execute('''INSERT INTO PLAYERS(
    USER_NAME, UID, PASSWORD, SCORE) VALUES 
    ('Eric', '84567', '123456','20')''')

    # Commit my change
    conn.commit()

    # Fetch results
    results = cursor.fetchall()

    # print the results
    print(results)

    # Close the database connection
    conn.close()

    #"Records inserted...""
schema()

#CREATE
import sqlite3

def create():
    user_name = input("Enter your username:")
    uid = input("Enter your user id:")
    password = input("Enter your password:")
    score = input("Enter your Score:")
    
    # Connect to the database file
    conn = sqlite3.connect(database)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    try:
        # Execute an SQL command to insert data into a table
        cursor.execute("INSERT INTO PLAYERS (USER_NAME, UID, PASSWORD, SCORE) VALUES (?, ?, ?, ?)", (user_name, uid, password, score))
        
        # Commit the changes to the database
        conn.commit()
        print(f"A new user record {uid} has been created")
                
    except sqlite3.Error as error:
        print("Error while executing the INSERT:", error)


    # Close the cursor and connection objects
    cursor.close()
    conn.close()


#READ
import sqlite3

def read():
    # Connect to the database file
    conn = sqlite3.connect(database)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Execute a SELECT statement to retrieve data from a table
    results = cursor.execute('SELECT * FROM PLAYERS').fetchall()

    # Print the results
    if len(results) == 0:
        print("Table is empty")
    else:
        for row in results:
            print(row)

    # Close the cursor and connection objects
    cursor.close()
    conn.close()
    
read()

def update():
    uid = input("Enter user id to update")
    password = input("Enter updated password")
    if len(password) < 2:
        message = "Playground"
        password = 'playground'
    else:
        message = "successfully updated"

    # Connect to the database file
    conn = sqlite3.connect(database)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    try:
        # Execute an SQL command to update data in a table
        cursor.execute("UPDATE PLAYERS SET PASSWORD = ? WHERE UID = ?", (password, uid))
        if cursor.rowcount == 0:
            # The uid was not found in the table
            print(f"No uid {uid} was not found in the playground table")
        else:
            print(f"The row with user id {uid} the password has been {message}")
            conn.commit()
    except sqlite3.Error as error:
        print("Error while executing the UPDATE:", error)
        
    
    # Close the cursor and connection objects
    cursor.close()
    conn.close()

import sqlite3

#DELETE
def delete():
    uid = input("Enter user id to delete")

    # Connect to the database file
    conn = sqlite3.connect(database)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM PLAYERS WHERE UID = ?", (uid,))
        # get the number of rows affected.
        cursor.execute("SELECT changes()").fetchone()[0]
        
        conn.commit()
    except sqlite3.Error as error:
        print("Error while executing the DELETE:", error)
        
    # Close the cursor and connection objects
    cursor.close()
    conn.close()

def menu():
    operation = input("Enter: (C)reate (R)ead (U)pdate or (D)elete or (S)chema")
    if operation.lower() == 'c':
        create()
    elif operation.lower() == 'r':
        read()
    elif operation.lower() == 'u':
        update()
    elif operation.lower() == 'd':
        delete()
    elif operation.lower() == 's':
        schema()
    elif len(operation)==0: # Escape Key
        return
    else:
        print("Please enter c, r, u, or d") 
    menu() # recursion, repeat menu
        
try:
    menu() # start menu
except:
    print("Perform Jupyter 'Run All' prior to starting menu")

