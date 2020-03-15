import sqlite3
import validators
from tkinter import *
from tkinter import messagebox

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

conn=sqlite3.connect('passwords.db')
cursor=conn.cursor()
createTable()

def insertRecord():
    w=websiteEntry.get()
    e=emailEntry.get()
    p=passwordEntry.get()

    validEmail=validateEmail(e)
    validWebsite=validateWebsite(w)
    checkWeb=checkWebsite(w)

    if(checkWeb):
        messagebox.showerror("Website exists","Website already exists in table")

    if(not checkWeb and validEmail and validWebsite and w and p and e):
        clearRecords()
        try:
            cursor.execute("""INSERT INTO savedpasswords (website,email,password) VALUES (?,?,?)""",(w,e,p))
            conn.commit()
            messagebox.showinfo("Inserted record","The record has been inserted")
            print("Values added")
        except:
            print("Values not added")
            pass

def deleteRecord():
    w=websiteEntry.get()
    checkWeb=checkWebsite(w)
    if (not checkWeb):
        messagebox.showerror("Website does not exist","Website does not exist in table")

    if(checkWeb and w):
        clearRecords()
        try:
            cursor.execute("""DELETE FROM savedpasswords WHERE website=?""", (w,))
            conn.commit()
            messagebox.showinfo("Deleted record","The record has been deleted")
            print("Value deleted")
        except:
            print("Value not deleted")
            pass

def updateRecord():
    w=websiteEntry.get()
    e=emailEntry.get()
    p=passwordEntry.get()
    checkWeb=checkWebsite(w)
    if (not checkWeb):
        messagebox.showerror("Website does not exist","Website does not exist in table")

    if(checkWeb and w and (p or e)):
        try:
            if(p):
                cursor.execute("""UPDATE savedpasswords SET password=? WHERE website=?""",(p,w))
                conn.commit()
            if(e):
                validEmail=validateEmail(e)
                if(validEmail):
                    cursor.execute("""UPDATE savedpasswords SET email=? WHERE website=?""",(e,w))
                    conn.commit()
            messagebox.showinfo("Updated record","The record has been updated")
            clearRecords()
            displayRecord(w)
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
        tableWindow=Toplevel()
        tableWindow.wm_title("Display Table")
        tableWindow.iconbitmap("icon.ico")
        tableWindow.focus_set()

        f="{:30s}"
        str=f.format("Website:")
        heading1=Label(tableWindow,text=str,justify=LEFT,anchor=W)
        heading1.grid(sticky=W,row=0,column=0)
        str=f.format("Email:")
        heading2=Label(tableWindow,text=str,justify=LEFT,anchor=W)
        heading2.grid(sticky=W,row=0,column=1)
        str=f.format("Password:")
        heading3=Label(tableWindow,text=str,justify=LEFT,anchor=W)
        heading3.grid(sticky=W,row=0,column=2)
        count=1

        for row in websites:
            str=f.format(row[0])
            body1=Label(tableWindow,text=str,justify=LEFT,anchor=W)
            body1.grid(sticky=W,row=count,column=0)
            str=f.format(row[1])
            body2=Label(tableWindow,text=str,justify=LEFT,anchor=W)
            body2.grid(sticky=W,row=count,column=1)
            str=f.format(row[2])
            body3=Label(tableWindow,text=str,justify=LEFT,anchor=W)
            body3.grid(sticky=W,row=count,column=2)
            count+=1

        print("Table printed")
    except:
        print("Could not print table")
        pass

def displayRecord(w=""):
    if(not w):
        w=websiteEntry.get()
    checkWeb=checkWebsite(w)
    if (not checkWeb):
        messagebox.showerror("Website does not exist","Website does not exist in table")
    if(checkWeb):
        try:
            cursor.execute("""SELECT email FROM savedpasswords WHERE website=?""",(w,))
            emails=cursor.fetchone()
            conn.commit()
            cursor.execute("""SELECT password FROM savedpasswords WHERE website=?""",(w,))
            passwords=cursor.fetchone()
            conn.commit()
            str="Website: "+w+"\nEmail: "+emails[0]+"\nPassword: "+passwords[0]
            print("For "+w+": ")
            print("\tEmail: "+emails[0])
            print("\tPassword: "+passwords[0])
            extraLabel.config(text=str)
            extraLabel.grid(row=8,column=0,columnspan=2)
        except:
            print("Could not get website details")
            pass

def validateEmail(e):
    if(validators.email(e)):
        return True
    else:
        messagebox.showerror("Invalid email","Email address entered is invalid")
        return False

def validateWebsite(w):
    if(validators.url(w)):
        return True
    else:
        messagebox.showerror("Invalid URL","URL entered is invalid")
        return False

def clearRecords():
    websiteEntry.delete(0,END)
    emailEntry.delete(0,END)
    passwordEntry.delete(0,END)
    extraLabel.config(text="")

root=Tk()

root.iconbitmap("icon.ico")
root.wm_title("Password Manager")

homeFrame=Frame(root)
homeFrame.grid()

websiteLabel=Label(homeFrame,text="Website: ")
websiteLabel.grid(row=0,column=0,padx=10,pady=10)
websiteEntry=Entry(homeFrame,width=30)
websiteEntry.grid(row=0,column=1,padx=10,pady=10)

emailLabel=Label(homeFrame,text="Email: ")
emailLabel.grid(row=1,column=0,padx=10,pady=10)
emailEntry=Entry(homeFrame,width=30)
emailEntry.grid(row=1,column=1,padx=10,pady=10)

passwordLabel=Label(homeFrame,text="Password: ")
passwordLabel.grid(row=2,column=0,padx=10,pady=10)
passwordEntry=Entry(homeFrame,width=30)
passwordEntry.grid(row=2,column=1,padx=10,pady=10)

addBtn=Button(homeFrame,text="Add Record",command=insertRecord,width=30)
addBtn.grid(row=3,column=0,columnspan=2,padx=10,pady=10)
delBtn=Button(homeFrame,text="Delete Record",command=deleteRecord,width=30)
delBtn.grid(row=4,column=0,columnspan=2,padx=10,pady=10)
updBtn=Button(homeFrame,text="Update Record",command=updateRecord,width=30)
updBtn.grid(row=5,column=0,columnspan=2,padx=10,pady=10)
disRecBtn=Button(homeFrame,text="Display Record",command=displayRecord,width=30)
disRecBtn.grid(row=6,column=0,columnspan=2,padx=10,pady=10)
disTblBtn=Button(homeFrame,text="Display Table",command=displayTable,width=30)
disTblBtn.grid(row=7,column=0,columnspan=2,padx=10,pady=10)
extraLabel=Label(homeFrame)

root.mainloop()
