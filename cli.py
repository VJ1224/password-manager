import sqlite3
import validators

conn=sqlite3.connect('passwords.db')
cursor=conn.cursor()

def createTable():
    try:
        cursor.execute("""CREATE TABLE savedpasswords
               (website VARCHAR,
               email VARCHAR,
               password VARCHAR)""")
        conn.commit()
        print("Table created successfully")
    except:
        print("Table exists")
        pass

def insertRecord(w,e,p):
    try:
        cursor.execute("""INSERT INTO savedpasswords (website,email,password)
        VALUES (?,?,?)""",(w,e,p))
        conn.commit()
        print("Values added")
    except:
        print("Values not added")
        pass

def deleteRecord(w):
    try:
        cursor.execute("""DELETE FROM savedpasswords WHERE website=?""", (w,))
        conn.commit()
        print("Value deleted")
    except:
        print("Value not deleted")
        pass

def updateRecord(w,e,p):
    try:
        if(validateEmail(e)):
            cursor.execute("""UPDATE savedpasswords SET email=?,password=? WHERE website=?""",(e,p,w))
            conn.commit()
            print("Value updated")
    except:
        print("Value not updated")
        pass

def checkWebsite(w):
    try:
        cursor.execute("""SELECT website FROM savedpasswords WHERE website=?""",(w,))
        website=cursor.fetchone()
        conn.commit()
        if(len(website)>0):
            print("Website exists")
            return True
    except:
        print("Website does not exist")
        return False
        pass

def displayTable():
    try:
        cursor.execute("""SELECT * FROM savedpasswords""")
        websites=cursor.fetchall()
        conn.commit()
        print("{:25s}".format("Website:"),end="")
        print("{:30s}".format("Email:"),end="")
        print("{:20s}".format("Password:"))
        for row in websites:
            print("{:25s}".format(row[0]),end="")
            print("{:30s}".format(row[1]),end="")
            print("{:20s}".format(row[2]))
    except:
        print("Could not print table")
        pass

def displayRecord(w):
    try:
        cursor.execute("""SELECT email FROM savedpasswords WHERE website=?""",(w,))
        emails=cursor.fetchone()
        conn.commit()
        cursor.execute("""SELECT password FROM savedpasswords WHERE website=?""",(w,))
        passwords=cursor.fetchone()
        conn.commit()
        print("For "+w+": ")
        print("\tEmail: "+emails[0])
        print("\tPassword: "+passwords[0])
    except:
        print("Could not get website details")
        pass

def validateEmail(e):
    if(validators.email(e)):
        return True
    else:
        return False

def validateWebsite(w):
    if(validators.url(w)):
        return True
    else:
        return False

def inputWebsite():
    valid=True
    w=input("\nEnter website name: ")
    if(not validateWebsite(w)):
        valid=False
        print("Invalid url")
        return 0

    if(checkWebsite(w)):
        valid=False
        return 0

    e=input("Enter email address: ")
    if(not validateEmail(e)):
        valid=False
        print("Invalid email address")
        return 0

    p=input("Enter password: ")

    if(valid):
        insertRecord(w,e,p)
        return 1

def showMenu():
    print("\n\n1.Display table\n2.Display record\n3.Insert record\n4.Update record\n5.Delete record\n6.Stop")
    c=input("\nEnter choice: ")
    return c

def checkPassword():
    p=input("Enter master password: ")
    if(p=="vanshjain"):
        print("Correct password")
        return True
    else:
        print("Incorrect password")
        False

def main():
    createTable()
    login=checkPassword()
    while (login):
        c=showMenu()
        if(c=="1"):
            displayTable()
        elif(c=="2"):
            w=input("\nEnter website: ")
            if(checkWebsite(w)):
                displayRecord(w)
        elif(c=="3"):
            inputWebsite()
        elif(c=="4"):
            w=input("\nEnter website: ")
            if(checkWebsite(w)):
                displayRecord(w)
                e=input("\nEnter new email: ")
                p=input("\nEnter new password: ")
                updateRecord(w,e,p)
        elif(c=="5"):
            w=input("\nEnter website: ")
            if(checkWebsite(w)):
                deleteRecord(w)
        elif(c=="6"):
            exit()

if __name__ == '__main__':
    main()
