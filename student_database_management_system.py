import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

mywindow = tk.Tk()
mywindow.title("Management")

mywindow.geometry("660x350")
mywindow.resizable(0, 0)

connection = sqlite3.connect('info.db')

TABLE_NAME = "student_table"
STUDENT_ID = "student_id"
STUDENT_NAME = "student_name"
STUDENT_COLLEGE = "student_college"
STUDENT_ADDRESS = "student_address"
STUDENT_PHONE = "student_phone"

connection.execute(" CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ( " + STUDENT_ID +
                   " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                   STUDENT_NAME + " TEXT, " + STUDENT_COLLEGE + " TEXT, " +
                   STUDENT_ADDRESS + " TEXT, " + STUDENT_PHONE + " INTEGER);")

mainLabel = tk.Label(mywindow, text="STUDENT MANAGEMENT SYSTEM", fg="#555599", width=30)
mainLabel.config(font=("Franklin Gothic Medium", 30))
mainLabel.grid(row=0, columnspan=2, padx=(10, 10), pady=(30, 0))

nameLabel = tk.Label(mywindow, text="ENTER YOUR NAME", width=40, anchor='w',
                     font=("Sylfaen", 12)).grid(row=1, column=0, padx=(50, 0), pady=(30, 0))

collegeLabel = tk.Label(mywindow, text="ENTER YOUR COLLEGE", width=40, anchor='w',
                        font=("Sylfaen", 12)).grid(row=2, column=0, padx=(50, 0))

addressLabel = tk.Label(mywindow, text="ENTER YOUR ADDRESS", width=40, anchor='w',
                        font=("Sylfaen", 12)).grid(row=3, column=0, padx=(50, 0))

phoneLabel = tk.Label(mywindow, text="ENTER YOUR PHONE NO.", width=40, anchor='w',
                      font=("Sylfaen", 12)).grid(row=4, column=0, padx=(50, 0))

nameEntry = tk.Entry(mywindow, width=30)
collegeEntry = tk.Entry(mywindow, width=30)
addressEntry = tk.Entry(mywindow, width=30)
phoneEntry = tk.Entry(mywindow, width=30)

nameEntry.grid(row=1, column=1, padx=(0, 40), pady=(30, 10))
collegeEntry.grid(row=2, column=1, padx=(0, 40), pady=10)
addressEntry.grid(row=3, column=1, padx=(0, 40), pady=10)
phoneEntry.grid(row=4, column=1, padx=(0, 40), pady=10)


def takeNameInput():
    username = nameEntry.get()
    nameEntry.delete(0, tk.END)
    collegeName = collegeEntry.get()
    collegeEntry.delete(0, tk.END)
    address = addressEntry.get()
    addressEntry.delete(0, tk.END)
    phone = int(phoneEntry.get())
    phoneEntry.delete(0, tk.END)

    connection.execute("INSERT INTO " + TABLE_NAME + " ( " + STUDENT_NAME + ", " +
                       STUDENT_COLLEGE + ", " + STUDENT_ADDRESS + ", " +
                       STUDENT_PHONE + " ) VALUES ( '"
                       + username + "', '" + collegeName + "', '" +
                       address + "', " + str(phone) + " ); ")
    connection.commit()
    messagebox.showinfo("Success", "Data Saved Successfully.")


def destroyRootWindow():
    mywindow.destroy()
    secondWindow = tk.Tk()

    # secondWindow.geometry("660x300")
    # secondWindow.resizable(0, 0)

    secondWindow.title("CURRENT RECORDS")

    appLabel = tk.Label(secondWindow, text="Student Management System",
                        fg="#06a099", width=40)
    appLabel.config(font=("Sylfaen", 30))
    appLabel.pack()

    tree = ttk.Treeview(secondWindow)
    tree["columns"] = ("one", "two", "three", "four")

    tree.heading("one", text="Student Name")
    tree.heading("two", text="College Name")
    tree.heading("three", text="Address")
    tree.heading("four", text="Phone Number")

    cursor = connection.execute("SELECT * FROM " + TABLE_NAME + " ;")
    i = 0

    for row in cursor:
        tree.insert('', i, text="Student " + str(row[0]),
                    values=(row[1], row[2],
                            row[3], row[4]))
        i = i + 1

    tree.pack()
    secondWindow.mainloop()


button = tk.Button(mywindow, text="INSERT", activebackground="gray", width=20, command=lambda: takeNameInput())
button.grid(row=5, column=0, pady=30)

displayButton = tk.Button(mywindow, text="DISPLAY", activebackground="gray", width=20,
                          command=lambda: destroyRootWindow())
displayButton.grid(row=5, padx=(10, 100), column=1)

mywindow.mainloop()
