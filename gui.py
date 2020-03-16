import sqlite3
import validators
import csv
import hash
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font

#Creates a databse and a table if does not exist
def createTable():
    try:
        cursor.execute("""CREATE TABLE savedpasswords
               (website VARCHAR,
               email VARCHAR,
               password VARCHAR)""")
        conn.commit()
    except:
        pass

#Creates connection to database
conn=sqlite3.connect('passwords.db')
cursor=conn.cursor()
createTable()

#Inserts a new record
def insertRecord():
    w=websiteEntry.get()
    e=emailEntry.get()
    p=passwordEntry.get()

    #Validates email and website
    validEmail=validateEmail(e)
    validWebsite=validateWebsite(w)

    checkWeb=checkWebsite(w)

    #Checks if password field is not empty
    if (not p):
        messagebox.showerror("Check password","Invalid password")

    #Checks if website is not already entered in table
    if(checkWeb):
        messagebox.showerror("Check website","Website already exists")

    #Adds record if all validation checks are true
    if(not checkWeb and validEmail and validWebsite and w and p and e):
        clearRecords()
        try:
            cursor.execute("""INSERT INTO savedpasswords (website,email,password) VALUES (?,?,?)""",(w,e,p))
            conn.commit()
            messagebox.showinfo("Inserted record","Record inserted successfully")
        except:
            pass

#Deletes a record
def deleteRecord():
    w=websiteEntry.get()

    #Checks if website is entered in table
    checkWeb=checkWebsite(w)
    if (not checkWeb):
        messagebox.showerror("Check website","Website does not exist")

    #Finds the website and deletes if it exists
    if(checkWeb and w):
        clearRecords()
        try:
            cursor.execute("""DELETE FROM savedpasswords WHERE website=?""", (w,))
            conn.commit()
            messagebox.showinfo("Deleted record","Record deleted successfully")
        except:
            pass

#Updates a record
def updateRecord():
    w=websiteEntry.get()
    e=emailEntry.get()
    p=passwordEntry.get()

    #Checks if website is entered in table
    checkWeb=checkWebsite(w)
    if (not checkWeb):
        messagebox.showerror("Check website","Website does not exist")

    #Checks if password field is not empty
    if (not p):
        messagebox.showerror("Check password","Invalid password")

    #Updates the record if validation checks are true
    if(checkWeb and w and (p or e)):
        try:
            #Updates password if password is entered
            if(p):
                cursor.execute("""UPDATE savedpasswords SET password=? WHERE website=?""",(p,w))
                conn.commit()
            #Updates email if email is entered
            if(e):
                validEmail=validateEmail(e)
                if(validEmail):
                    cursor.execute("""UPDATE savedpasswords SET email=? WHERE website=?""",(e,w))
                    conn.commit()
            messagebox.showinfo("Updated record","Record updated successfully")
            clearRecords()
            displayRecord(w)
        except:
            pass

#Checks if website is present in table
def checkWebsite(w):
    try:
        cursor.execute("""SELECT website FROM savedpasswords WHERE website=?""",(w,))
        website=cursor.fetchone()
        conn.commit()
        if(len(website)>0):
            return True
    except:
        return False
        pass

#Displays all records in a table
def displayTable():
    try:
        cursor.execute("""SELECT * FROM savedpasswords""")
        websites=cursor.fetchall()
        conn.commit()

        #Creates a new window to display table
        tableWindow=Toplevel()
        tableWindow.resizable(0,0)
        tableWindow.wm_title("Display Table")
        tableWindow.iconbitmap("icon.ico")
        tableWindow.focus_set()

        #Formats all strings to length 30 for equal width columns
        f="{:30s}"

        #Adds headings
        str=f.format("Website:")
        heading1=Label(tableWindow,text=str,justify=LEFT,anchor=W)
        heading1.grid(sticky=W,row=0,column=0)
        str=f.format("Email:")
        heading2=Label(tableWindow,text=str,justify=LEFT,anchor=W)
        heading2.grid(sticky=W,row=0,column=1)
        str=f.format("Password:")
        heading3=Label(tableWindow,text=str,justify=LEFT,anchor=W)
        heading3.grid(sticky=W,row=0,column=2)

        #Adds a new row with all fields
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
    except:
        pass

#Displays a single record
def displayRecord(w=""):

    #If website parameter is not given takes it from entry
    if(not w):
        w=websiteEntry.get()

    #Checks if website exists in table
    checkWeb=checkWebsite(w)
    if (not checkWeb):
        messagebox.showerror("Check website","Website does not exist")

    #Displays details if website exists
    if(checkWeb):
        try:
            cursor.execute("""SELECT email FROM savedpasswords WHERE website=?""",(w,))
            emails=cursor.fetchone()
            conn.commit()
            cursor.execute("""SELECT password FROM savedpasswords WHERE website=?""",(w,))
            passwords=cursor.fetchone()
            conn.commit()
            str="Website: "+w+"\nEmail: "+emails[0]+"\nPassword: "+passwords[0]
            extraLabel.config(text=str)
            extraLabel.grid(row=9,column=0,columnspan=2)
        except:
            pass

#Download table as .csv file
def downloadCSV():
    cursor.execute("""SELECT * FROM savedpasswords""")
    websites=cursor.fetchall()
    conn.commit()

    #Python csv module
    writer=csv.writer(open("passwords.csv","w",newline=""))
    writer.writerow(("Websites","Emails","Passwords"))

    #Writes each row
    for row in websites:
        writer.writerow(row)

    messagebox.showinfo("Download as CSV","Download successful")

#Uses validators mdoule to validate email
def validateEmail(e):
    if(validators.email(e)):
        return True
    else:
        messagebox.showerror("Check email","Invalid email address")
        return False

#Uses validators mdoule to validate website URL
def validateWebsite(w):
    if(validators.url(w)):
        return True
    else:
        messagebox.showerror("Check URL","Invalid website URL")
        return False

#Sets all entry fields to empty, removes any records displayed
def clearRecords():
    websiteEntry.delete(0,END)
    emailEntry.delete(0,END)
    passwordEntry.delete(0,END)
    extraLabel.config(text="")

#Verifies master passwords
def checkMasterPassword(event=None):
    password=masterEntry.get()
    if(encrypt.verifyPassword(password)):
        #Destroys master password entry window
        masterWindow.destroy()
        #Shows main window
        root.deiconify()
    else:
        messagebox.showerror("Incorrect Password","Incorrect password")

#Creates root window
root=Tk()
root.resizable(0,0)
root.iconbitmap("icon.ico")
root.wm_title("Password Manager")
root.withdraw()

#Changes the default font
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=9,family="Arial")

#Creates window to enter master password
masterWindow=Toplevel()
masterWindow.resizable(0,0)
masterWindow.wm_title("Enter password")
masterWindow.iconbitmap("icon.ico")
masterWindow.focus_set()

#Adds widgets for master password entry
masterLabel=Label(masterWindow,text="Enter password:",)
masterLabel.grid(row=0,column=0,padx=10,pady=10)
masterEntry=Entry(masterWindow,width=30,show="*")
masterEntry.grid(row=1,column=0,padx=10,pady=10)
masterBtn=Button(masterWindow,text="Submit",command=checkMasterPassword,width=30)
masterWindow.bind('<Return>', checkMasterPassword)
masterBtn.grid(row=2,column=0,columnspan=2,padx=10,pady=10)
masterWindow.focus_set()

#Creates main window frame
homeFrame=Frame(root)
homeFrame.grid()

#Adds widgets for website entry
websiteLabel=Label(homeFrame,text="Website: ")
websiteLabel.grid(row=0,column=0,)
websiteEntry=Entry(homeFrame,width=30)
websiteEntry.grid(row=0,column=1,padx=10,pady=10)

#Adds widgets for email entry
emailLabel=Label(homeFrame,text="Email: ")
emailLabel.grid(row=1,column=0,padx=10,pady=10)
emailEntry=Entry(homeFrame,width=30)
emailEntry.grid(row=1,column=1,padx=10,pady=10)

#Adds widgets for password entry
passwordLabel=Label(homeFrame,text="Password: ")
passwordLabel.grid(row=2,column=0,padx=10,pady=10)
passwordEntry=Entry(homeFrame,width=30,show="*")
passwordEntry.grid(row=2,column=1,padx=10,pady=10)


#Adds buttons for all functions
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
downCSVBtn=Button(homeFrame,text="Download as CSV",command=downloadCSV,width=30)
downCSVBtn.grid(row=8,column=0,columnspan=2,padx=10,pady=10)
#Extra label that displays record details
extraLabel=Label(homeFrame)

root.mainloop()
