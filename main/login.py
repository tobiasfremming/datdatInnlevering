import sqlite3 as sql
from sqlite3 import Error
import hashlib 
import cleanCommands as command

def hashInput(string):
    hashed = (hashlib.sha256(string.encode()))
    hex_dig = hashed.hexdigest()
    return hex_dig

def logIn():
    try:
        connection = sql.connect(command.db_file())
        cursor = connection.cursor()
        print("Skriv din e-postadresse:")
        mail = command.cleanInput(str)
        print("Skriv ditt passord: ")
        password = command.cleanInput(str)
        password = hashInput(password)
        
        cursor.execute("SELECT email, passord, navn FROM Bruker WHERE email = ?", (mail,))
        data=cursor.fetchall()
        if len(data)!=0:
            if(data[0][0]==mail and data[0][1]==password):
                print("Velkommen " + data[0][2] + "!")
                return data
            else:
                print("feil passord")
                return None
        else:
            print("Ikke gyldig innlogging")
            return None

    except Error as e:
        print(e)




def newUser():
    print("epost:")
    email = command.cleanInput(str)
    print("fullt navn:")
    name = command.cleanInput(str)
    print("passord:")
    password = command.cleanInput(str)
    password = hashInput(password)

    connection = None
    try:

        connection = sql.connect(command.db_file())
        print(sql.version)
        cursor = connection.cursor()

        cursor.execute("SELECT email FROM Bruker WHERE email = ?", (email,))
        data=cursor.fetchall()

        if len(data)==0:
            cursor.execute("""INSERT INTO Bruker (email, navn, passord) VALUES (?,?,?);
            """, (email, name, password))
        
            connection.commit()

            cursor.execute("SELECT email FROM Bruker WHERE email = ?", (email,))
            newData=cursor.fetchall()
            if len(newData) != 0:
                print("vellykket!")
        
        else:
            print("Brukeren finnes alt")
            
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()



def changePassword(email, password):

    password = hashInput(password)
    connection = None

    try:
        connection = sql.connect(command.db_file())
        print(sql.version)
        cursor = connection.cursor()

        cursor.execute("SELECT email FROM Bruker WHERE email = ?", (email,))
        data=cursor.fetchall()

        if len(data)!=0:
            cursor.execute("""UPDATE Bruker SET passord = ? WHERE email = ?;
            """, (password, email))
        
            connection.commit()
            print("vellykket")
            cursor.execute("SELECT passord FROM Bruker WHERE email = ?", (email,))
            data=cursor.fetchall()
            print(data)
            
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


