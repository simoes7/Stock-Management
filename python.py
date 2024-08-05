from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import pymysql
import csv
from datetime import datetime
import numpy as np

window = tkinter.Tk()
window.title("STOCK MANAGEMENT SYSTEM")
window.geometry("720x640")
my_tree = ttk.Treeview(window, show='headings', height=20)
style = ttk.Style()


placeholderArray = ['', '', '', '', '']

for i in range(0, 5):
    placeholderArray[i]=tkinter.StringVar()

#functions :
def Ajouter():
    itemId = itemIdEntry.get()
    name = nameEntry.get()
    price = priceEntry.get()
    quantity = qntEntry.get()
    category = categoryCombo.get()

    if itemId and name and price and quantity and category:
        try:
            cnx = pymysql.connect(host='localhost', user='root', password='', database='product_management')
            with cnx.cursor() as cursor:
                # Check if item_id already exists
                check_sql = "SELECT COUNT(*) FROM products WHERE item_id = %s"
                cursor.execute(check_sql, (itemId,))
                result = cursor.fetchone()
                if result[0] > 0:
                    messagebox.showwarning("Warning", f"Item ID '{itemId}' already exists.")
                else:
                    # Insert new record into the database
                    insert_sql = "INSERT INTO products (item_id, name, price, quantity, category) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(insert_sql, (itemId, name, price, quantity, category))
                    cnx.commit()
                    messagebox.showinfo("Success", "Record added successfully.")
                    afficher()  # Refresh the Treeview after adding a new record
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error adding record: {e}")
        finally:
            cnx.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")


def afficher():
    cnx = pymysql.connect(host='localhost', user='root', password='', database='product_management')
    with cnx.cursor() as cursor:
        sql = "SELECT * FROM products order by item_id"
        cursor.execute(sql)
        rows = cursor.fetchall()

    # Clear existing rows from Treeview
    for row_id in my_tree.get_children():
        my_tree.delete(row_id)

    # Insert fetched data into Treeview
    for row in rows:
        my_tree.insert("", "end", values=row)

    cnx.close()

def Update():
    itemId = itemIdEntry.get()
    name = nameEntry.get()
    price = priceEntry.get()
    quantity = qntEntry.get()
    category = categoryCombo.get()

    if itemId and name and price and quantity and category:
        try:
            cnx = pymysql.connect(host='localhost', user='root', password='', database='product_management')
            with cnx.cursor() as cursor:
                # Check if item_id exists
                check_sql = "SELECT COUNT(*) FROM products WHERE item_id = %s"
                cursor.execute(check_sql, (itemId,))
                result = cursor.fetchone()
                if result[0] == 0:
                    messagebox.showwarning("Warning", f"Item ID '{itemId}' does not exist.")
                else:
                    # Update record in the database
                    update_sql = "UPDATE products SET name = %s, price = %s, quantity = %s, category = %s WHERE item_id = %s"
                    cursor.execute(update_sql, (name, price, quantity, category, itemId))
                    cnx.commit()
                    messagebox.showinfo("Success", "Record updated successfully.")
                    afficher()  # Refresh the Treeview after updating the record
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            cnx.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")
    itemId = ''
    name = ''
    price = ''
    quantity = ''
    category = ''

def Delete():
    itemId = itemIdEntry.get()

    if itemId:
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record with ID '{itemId}'?")
        if confirm:
            try:
                cnx = pymysql.connect(host='localhost', user='root', password='', database='product_management')
                with cnx.cursor() as cursor:
                    # Check if item_id exists
                    check_sql = "SELECT COUNT(*) FROM products WHERE item_id = %s"
                    cursor.execute(check_sql, (itemId,))
                    result = cursor.fetchone()
                    if result[0] == 0:
                        messagebox.showwarning("Warning", f"Item ID '{itemId}' does not exist.")
                    else:
                        # Delete record from the database
                        delete_sql = "DELETE FROM products WHERE item_id = %s"
                        cursor.execute(delete_sql, (itemId,))
                        cnx.commit()
                        messagebox.showinfo("Success", f"Record with ID '{itemId}' deleted successfully.")
                        afficher()  # Refresh the Treeview after deleting the record
            except pymysql.Error as e:
                messagebox.showerror("Error", f"Error deleting record: {e}")
            finally:
                cnx.close()
    else:
        messagebox.showwarning("Warning", "Please enter an Item ID.")


def Find():
    itemId = itemIdEntry.get()

    if itemId:
        try:
            cnx = pymysql.connect(host='localhost', user='root', password='', database='product_management')
            with cnx.cursor() as cursor:
                # Check if item_id exists
                check_sql = "SELECT COUNT(*) FROM products WHERE item_id = %s"
                cursor.execute(check_sql, (itemId,))
                result = cursor.fetchone()
                if result[0] == 0:
                    messagebox.showwarning("Warning", f"Item ID '{itemId}' does not exist.")
                else:
                    # Fetch the record with the specified item_id
                    select_sql = "SELECT * FROM products WHERE item_id = %s"
                    cursor.execute(select_sql, (itemId,))
                    row = cursor.fetchone()
                    # Clear existing rows from Treeview
                    for row_id in my_tree.get_children():
                        my_tree.delete(row_id)
                    # Insert fetched data into Treeview
                    my_tree.insert("", "end", values=row)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error finding record: {e}")
        finally:
            cnx.close()
    else:
        messagebox.showwarning("Warning", "Please enter an Item ID.")

def generate_id():
    try:
        cnx = pymysql.connect(host='localhost', user='root', password='', database='product_management')
        with cnx.cursor() as cursor:
            while True:
                # Generate a random ID
                random_id = str(random.randint(10000, 99999))
                # Check if the generated ID already exists in the database
                check_sql = "SELECT COUNT(*) FROM products WHERE item_id = %s"
                cursor.execute(check_sql, (random_id,))
                result = cursor.fetchone()
                if result[0] == 0:
                    itemIdEntry.delete(0, END)
                    itemIdEntry.insert(0, random_id)
                    break
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error generating ID: {e}")
    finally:
        cnx.close()


frame = tkinter.Frame(window, bg="#02577A")
frame.pack()

btnColor = "#196E78"

manageFrame = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
manageFrame.grid(row=0, column=0, sticky="w", padx=[10,200], pady=20, ipadx=[6])


saveBtn = Button(manageFrame, text="ADD", width=10, borderwidth=3, bg=btnColor, fg='white', command = Ajouter)
updateBtn = Button(manageFrame, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='white', command=Update)
deleteBtn = Button(manageFrame, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='white', command=Delete)
selectBtn = Button(manageFrame, text="SELECT ALL", width=10, borderwidth=3, bg=btnColor, fg='white',command=afficher)
findBtn = Button(manageFrame, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='white', command=Find)
# clearBtn = Button(manageFrame, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='white')
# exportBtn = Button(manageFrame, text="EXPORT", width=10, borderwidth=3, bg=btnColor, fg='white')

saveBtn.grid(row=0, column=0, padx=5, pady=5)
updateBtn.grid(row=0, column=1, padx=5, pady=5)
deleteBtn.grid(row=0, column=2, padx=5, pady=5)
selectBtn.grid(row=0, column=3, padx=5, pady=5)
findBtn.grid(row=0, column=4, padx=5, pady=5)
# clearBtn.grid(row=0, column=5, padx=5, pady=5)
# exportBtn.grid(row=0, column=6, padx=5, pady=5)


entriesFrame = tkinter.LabelFrame(frame, text="Form", borderwidth=5)
entriesFrame.grid(row=1, column=0, sticky="w", padx=[10,200], pady=[0,20], ipadx=[6])

itemIdLabel = Label(entriesFrame, text="ITEM ID", anchor="e", width=10)
nameLabel = Label(entriesFrame, text="NAME", anchor="e", width=10)
priceLabel = Label(entriesFrame, text="PRICE", anchor="e", width=10)
qntLabel = Label(entriesFrame, text="QUANTITY", anchor="e", width=10)
categoryLabel = Label(entriesFrame, text="CATEGORY", anchor="e", width=10)

categoryArray = ['Perfume', 'Computer Parts', 'Make up', 'Glasses']

itemIdLabel.grid(row=0, column=0, padx=10)
nameLabel.grid(row=1, column=0, padx=10)
priceLabel.grid(row=2, column=0, padx=10)
qntLabel.grid(row=3, column=0, padx=10)
categoryLabel.grid(row=4, column=0, padx=10)


itemIdEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[0])
nameEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[1])
priceEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[2])
qntEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[3])
categoryCombo = ttk.Combobox(entriesFrame, width=47, textvariable=placeholderArray[4], values=categoryArray)

itemIdEntry.grid(row=0, column=1, padx=5, pady=5)
nameEntry.grid(row=1, column=1, padx=5, pady=5)
priceEntry.grid(row=2, column=1, padx=5, pady=5)
qntEntry.grid(row=3, column=1, padx=5, pady=5)
categoryCombo.grid(row=4, column=1, padx=5, pady=5)

generateIdBtn = Button(entriesFrame, text="GENERATE ID", borderwidth=3, bg=btnColor, fg='white', command=generate_id)
generateIdBtn.grid(row=0, column=2, padx=5, pady=5)

style.configure(window)

my_tree['columns'] = ("Item Id", "Name", "Price", "Quantity", "Category")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item Id", anchor=W, width=144)
my_tree.column("Name", anchor=W, width=144)
my_tree.column("Price", anchor=W, width=144)
my_tree.column("Quantity", anchor=W, width=144)
my_tree.column("Category", anchor=W, width=144)

my_tree.heading("Item Id", text="Item Id", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Category", text="Category", anchor=W)

my_tree.tag_configure('orow', background="#EEEEEE")
my_tree.pack()



afficher()


window.resizable(False, False)
window.mainloop()
