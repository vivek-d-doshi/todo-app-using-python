# This is to-do list app that can perform CRUD operations over entered task
# created by : Vivek Doshi
# resource used - VSC,Python,PostgreSQL
# Github - vivek-d-doshi 

from tkinter import Tk, Button, Scrollbar, Listbox, StringVar, W, E
from tkinter import ttk
from tkinter import messagebox

#for DB connection
import psycopg2 as psy
from dbconfig import dbcon

connection = psy.connect(**dbcon) # **name <--- to fetch whole data in name (dict,file)
print(connection)

cursor = connection.cursor()

#db inserting functions
class TodoApp():
    def __init__(self):
        self.connection = psy.connect(**dbcon)
        self.cursor = connection.cursor()
        print("You have connected to the Database")

    def __del__(self):
        self.connection.close()
    
    def insert(self,title):
        sql = ("INSERT INTO todo(title) VALUES (%s)")
        values = [title]
        self.cursor.execute(sql,values)
        self.connection.commit()
        messagebox.showinfo(title="Todolist Database",message="New Task added to database")

    def update(self, id, title):
        tsql = 'UPDATE todo SET title = %s WHERE id=%s'
        self.cursor.execute(tsql, [title,id])
        self.connection.commit()
        messagebox.showinfo(title="Todolist Databse", message="Task Updated")
    
    def delete(self,id):
        delquery = 'DELETE FROM todo WHERE id= %s'
        self.cursor.execute(delquery, [id])
        self.connection.commit()
        messagebox.showinfo(title="Todolist Databse", message="Task Deleted")
    
    def view(self):
        self.cursor.execute("SELECT * FROM todo")
        rows = self.cursor.fetchall()
        return rows


db = TodoApp()

# functions binded with UI
def get_selected_row(self):
    global selected_task
    index = list_bx.curselection()[0]
    selected_task = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_task[1])

def view_records():
    list_bx.delete(0,'end')
    for row in db.view():
        list_bx.insert('end', row)

def add_book():
    db.insert(title_text.get())
    list_bx.delete(0,'end')
    list_bx.insert('end', (title_text.get()))
    title_entry.delete(0, 'end')
    connection.commit()
    view_records()
    clear_screen()

def delete_task():
    db.delete(selected_task[0])
    connection.commit()
    view_records()
    clear_screen()

def clear_screen():
    title_entry.delete(0,'end')

def update_records():
    db.update(selected_task[0], title_text.get())
    title_entry.delete(0,"end")
    connection.commit()
    view_records()
    clear_screen()



# UI starts here
root = Tk()

root.title("TO-DO List App")

root.configure(background="#ECD9BA")
root.geometry("350x500")
root.resizable(width=False,height=False)

title_label = ttk.Label(root,text="Title",background="#DEC19B",font=("TkDefaultFont", 12))
title_label.grid(row=0,column=1,sticky=W,padx=25)
title_text = StringVar()
title_entry = ttk.Entry(root,width=25,textvariable=title_text)
title_entry.grid(row=0, column=2, sticky=W,pady=7)

#add button to add records
add_btn = Button(root,text="Add",bg="skyblue",fg="white",font="helvatica 10 bold",command=add_book)
add_btn.grid(row=0,column=3,sticky=W)


#creating list box
list_bx = Listbox(root,height=10,width=35,font="helvetica 13",bg="#FFFAF1")
list_bx.grid(row=3, column=1, columnspan=15, sticky=W + E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)
# scrollbar 
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=8,rowspan=11,sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

#buttons to edits
modify_btn = Button(root,text="Edit",bg="grey",fg="white",font="helvatica 10 bold",command=update_records)
modify_btn.grid(row=15,column=1)

delete_btn = Button(root,text="Delete",bg="red",fg="white",font="helvatica 10 bold",command=delete_task)
delete_btn.grid(row=15,column=2,padx=15)

exit_btn = Button(root,text="Exit",bg="black",fg="white",font="helvatica 10 bold",command=root.destroy)
exit_btn.grid(row=15,column=3,padx=10)

view_records()
root.mainloop()