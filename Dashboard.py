from sqlite3 import Row
from tabnanny import check
import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk
from tkinter import *
from ctypes import windll
from tkinter import filedialog
import os
import sys
from types import CellType
import pymysql
import xlrd
import csv
import pandas as pd
import MySQLdb
from tkinter import messagebox
import mysql.connector
import webbrowser
from PIL import Image, ImageTk
import matplotlib.pyplot as plt  
target = int
clicked = 0
input_clicked = 0
output_clicked = 0
visualize = 0

def login_screen():
    # get login name
    def login_name():
        return login.get()
    # register window

    def register_action(event):

        # return button pressed
        def out_action(event):
            register_main.destroy()
            login_screen()

        # signup button pressed
        def done_action(event):
            # database saved
            email_required = '@gmail.com'
            if confirm_password_set.get() != password_reg_set.get() and len(confirm_password_set.get()) != 0 and len(password_reg_set.get()) != 0:
                warning_window = tk.Tk()
                warning_window.geometry('360x60+900+300')
                warning_window.title('Warning')
                warning_window.resizable(False, False)
                unmatched = ttk.Label(warning_window, text='Passwords do not match',
                                      foreground='red', font=('Segoe UI', 10, 'italic'))
                unmatched.place(x=110, y=20)
                warning_window.mainloop()
            elif changed.get() == 0:
                warning_window = tk.Tk()
                warning_window.geometry('360x60+900+300')
                warning_window.title('Warning')
                warning_window.resizable(False, False)
                term_warning = ttk.Label(
                    warning_window, text='You need to agree with our Terms and Conditions ', foreground='red', font=('Segoe UI', 10, 'italic'))
                term_warning.place(x=48, y=20)
                warning_window.mainloop()
            elif len(confirm_password_set.get()) == 0 or len(password_reg_set.get()) == 0 or len(email_set.get()) == 0 or len(username_set.get()) == 0:
                warning_window = tk.Tk()
                warning_window.geometry('360x60+900+300')
                warning_window.title('Warning')
                warning_window.resizable(False, False)
                missing_warning = ttk.Label(
                    warning_window, text='Field(s) required', foreground='red', font=('Segoe UI', 12, 'italic'))
                missing_warning.place(x=128, y=20)
                warning_window.mainloop()
            elif email_required not in email_set.get():
                warning_window = tk.Tk()
                warning_window.geometry('360x60+900+300')
                warning_window.title('Warning')
                warning_window.resizable(False, False)
                mail_format = ttk.Label(warning_window, text='Email format is incorrect or not supported', font=(
                    'Segoe UI', 10, 'italic'), foreground='red')
                mail_format.place(x=65, y=20)
                warning_window.mainloop()
            else:
                reg = "INSERT INTO login (email,username,password_text) VALUES (%s,%s,%s)"
                login_val = (email_set.get(), username_set.get(),
                             password_reg_set.get())
                cursor.execute(reg, login_val)
                login_info.commit()
                register_main.destroy()
                login_screen()

        # register window
        root.destroy()
        register_main = tk.Tk()
        register_main.title("Register")
        register_main.resizable(width=False, height=False)
        register_main.geometry('320x240+850+250')
        email = ttk.Label(register_main, text='Email: ',
                          font=('Segoe UI', 10, 'bold'))
        email.pack()
        email.place(x=10, y=7)
        email_set = ttk.Entry(register_main)
        email_set.pack(pady=10, ipadx=10)
        username = ttk.Label(register_main, text="Username:",
                             font=('Segoe UI', 10, 'bold'))
        username.pack()
        username.place(x=10, y=50)
        username_set = ttk.Entry(register_main)
        username_set.pack(pady=10, ipadx=10)
        password_reg = ttk.Label(
            register_main, text="Password:", font=('Segoe UI', 10, 'bold'))
        password_reg.pack()
        password_reg.place(x=10, y=90)
        password_reg_set = ttk.Entry(register_main)
        password_reg_set.pack(pady=10, ipadx=10)
        confirm_password = ttk.Label(
            register_main, text="Confirm \nPassword:", font=('Segoe UI', 10, 'bold'))
        confirm_password.pack()
        confirm_password.place(x=10, y=115)
        confirm_password_set = ttk.Entry(register_main)
        confirm_password_set.pack(pady=10, ipadx=10)
        changed = IntVar(register_main)
        changed.set(0)
        check = tk.Checkbutton(register_main, variable=changed, onvalue=1, offvalue=0,
                               text='I agree with the terms and conditions of services.', fg='blue')
        check.pack()
        done = ttk.Button(register_main, text='Sign up', cursor='hand2')
        done.bind('<Button>', done_action)
        done.place(x=180, y=190, height=40, width=100)
        out = ttk.Button(register_main, text='Return', cursor='hand2')
        out.bind('<Button>', out_action)
        out.place(x=40, y=190, height=40, width=100)
        register_main.mainloop()

    # login function
    def login_action(event):
        global target
        command = str(
            "SELECT password_text FROM login_info.login WHERE username = '{}'").format(login.get())
        cursor.execute(command)
        result_pass = cursor.fetchone()
        if not login.get() or not password.get():
            not_found = tk.Tk()
            not_found.geometry('360x60+900+300')
            not_found.title('Login Checker')
            not_found.resizable(False, False)
            status = tk.Label(not_found, text='Username/Password is missing!',
                              font=('Segoe UI', 12), foreground='red')
            status.place(x=70, y=13)
            not_found.mainloop()
        elif not result_pass:
            not_found = tk.Tk()
            not_found.geometry('360x60+900+300')
            not_found.title('Login Checker')
            not_found.resizable(False, False)
            status = tk.Label(not_found, text='Username/Password is incorrect!',
                              font=('Segoe UI', 12), foreground='red')
            status.place(x=70, y=13)
            not_found.mainloop()
        elif result_pass[0] == password.get():
            command = str("SELECT id FROM login_info.login WHERE username = '{}' AND password_text = '{}'").format(
                login.get(), password.get())
            cursor.execute(command)
            result_id = cursor.fetchone()
            target = result_id[0]
            # create user database:
            database = mysql.connector.connect(
                host='localhost', user='root', password='Haido29904', database='login_info')
            cursor_2 = database.cursor()
            cursor_2.execute(
                "CREATE TABLE IF NOT EXISTS USER_NO_{}(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price INT, quantity INT, tag VARCHAR(255), total_value INT)".format(str(target)))
            cursor_2.execute('SET SQL_SAFE_UPDATES = 0')
            root.destroy()
            dashboard()
        else:
            fail = tk.Tk()
            fail.geometry('360x60+900+300')
            fail.title('Login Checker')
            fail.resizable(False, False)
            status = tk.Label(fail, text='Username/Password is incorrect!',
                              font=('Segoe UI', 12), foreground='red')
            status.place(x=70, y=13)
            fail.mainloop()

    # database declared/created for login and register
    login_info = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Haido29904",
        database="login_info")
    cursor = login_info.cursor(buffered=True)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS login(id INT AUTO_INCREMENT PRIMARY KEY,email VARCHAR(255), username VARCHAR(255), password_text VARCHAR(255))")
    # main window
    root = tk.Tk()
    root.geometry('320x240+850+250')
    root.resizable(False, False)
    root.title("Login")
    login_text = ttk.Label(text='Username', font=('Segoe UI', 12, 'bold'))
    login_text.pack()
    login = ttk.Entry()
    login.pack(ipadx=10, ipady=3)
    login.bind("<Return>", login_action)
    password_text = ttk.Label(text='Password', font=('Segoe UI', 12, 'bold'))
    password_text.pack()
    password = ttk.Entry(show='*')
    password.pack(ipadx=10, ipady=3)
    password.bind('<Return>', login_action)
    start_login = ttk.Button(text='Login', cursor='hand2')
    start_login.pack(anchor='center', pady=20, ipadx=5)
    start_login.bind('<Button>', login_action)
    register = ttk.Label(text='Register', font=(
        'Segoe UI', 12, 'italic', 'underline'), cursor='hand2')
    register.bind('<Button>', register_action)
    register.pack(anchor='center')
    root.mainloop()


# Dashboard
def dashboard():
    global target

    def menu_entry(event):
        global clicked
        if clicked % 2 == 0:
            menu.pack(ipadx=30)
            menu_icon.place(x=13)
            input_data.place_forget()
            update_data.place_forget()
            output_data.place_forget()
            graph_data.place_forget()
            log_out.place_forget()
            input_icon_label.place(x=5, y=110)
            center_icon_label.place(x=5, y=375)
            bar_icon_label.place(x=5, y=520)
            exit_icon_label.place(x=5, y=650)
            update_icon_label.place(x = 5, y = 240)
            clicked += 1
        else:
            input_icon_label.place_forget()
            center_icon_label.place_forget()
            bar_icon_label.place_forget()
            exit_icon_label.place_forget()
            update_icon_label.place_forget()
            menu_icon.place(x=260, y=73)
            menu.pack(side=LEFT, ipadx=150, ipady=350)
            input_data.place(x=0, y=110, height=60, width=304)
            update_data.place(x=0, y=240, height=60, width=304)
            output_data.place(x=0, y=380, height=60, width=304)
            graph_data.place(x=0, y=520, width=304, height=60)
            log_out.place(x=0, y=650, width=304, height=60)
            clicked += 1

        # Input function:
    def input_functions(event):
        global input_clicked
        global output_clicked
        global visualize
        # return button
        def return_action(event):
            global input_clicked
            input_clicked = 0
            frame.destroy()
            welcome_frame.pack()

        # main frame create:
        if input_clicked == 0 and output_clicked == 0 and visualize == 0:
            # Database for items
            welcome_frame.pack_forget()
            database = mysql.connector.connect(
            host='localhost', user='root', password='Haido29904', database='login_info')
            cursor_2 = database.cursor(buffered=True)
            def get_input(event):
                cursor_2.execute("SELECT name FROM user_no_{} WHERE name = '{}'".format(str(target), get_name.get()))
                check_exist = cursor_2.fetchone()
                if len(get_name.get()) == 0 or len(get_price.get()) == 0 or len(get_quantity.get()) == 0 or len(get_priority.get()) == 0:
                    messagebox.showwarning(
                        'Alert!', 'Field(s) required')
                elif not check_exist:
                    items = "INSERT INTO USER_NO_{}(name, price, quantity, tag) VALUES( %s, %s, %s, %s)".format(
                        str(target))
                    items_info = (get_name.get(), get_price.get(),
                                  get_quantity.get(), get_priority.get())
                    cursor_2.execute(items, items_info)
                    cursor_2.execute("UPDATE USER_NO_{} SET total_value = price * quantity".format(str(target)))
                    database.commit()       
                    messagebox.showinfo('Done!','Updated Successfully')
                elif check_exist[0] == get_name.get():
                    messagebox.showwarning('Alert!', 'Items exists!')
            frame = tk.Frame(root, background='#B1B2FF')

            # left bar:
            left = tk.Label(frame, background='#F29393')
            left.pack(side=LEFT, ipadx=10, ipady=1000)

            # right bar:
            right = ttk.Label(frame, background='#F29393')
            right.pack(side=RIGHT, ipadx=10, ipady=1000)

            # top bar:
            top = tk.Label(frame, background='#F29393')
            top.pack(side=TOP, ipadx=1000, ipady=5)

            # bottom bar:
            bottom = tk.Label(frame, background='#F29393')
            bottom.pack(side=BOTTOM, ipadx=1000, ipady=5)

            # Item name:
            name = ttk.Label(frame, text="Item's Name: ", font=(
                'Broken Console', 16, 'bold'), foreground = '#4169e1',background='#B1B2FF')
            name.place(relx=0.05, rely=0.12)
            get_name = ttk.Entry(frame, font=('Montserrat', 25))
            get_name.place(relx=0.3, rely=0.1, relwidth=0.6)

            # Item price:
            price = ttk.Label(frame, text="Item's Price: ", font=(
                'Broken Console', 16, 'bold'),foreground = '#4169e1', background='#B1B2FF')
            price.place(relx=0.05, rely=0.32)
            get_price = ttk.Entry(frame, font=('Montserrat', 25))
            get_price.place(relx=0.3, rely=0.3, relwidth=0.6)

            # Item quantity:
            quantity = ttk.Label(frame, text="Item's Quantity: ", font=(
                'Broken Console', 16, 'bold'), foreground = '#4169e1',background='#B1B2FF')
            quantity.place(relx=0.05, rely=0.52)
            get_quantity = ttk.Spinbox(frame, font=(
                'Montserrat', 25), from_=1, to=1000000, wrap=True)
            get_quantity.place(relx=0.3, rely=0.5, relwidth=0.6)

            # Item priority
            priority = ttk.Label(frame, text="Item's Priority: ", font=(
                'Broken Console', 16, 'bold'),foreground = '#4169e1', background='#B1B2FF')
            priority.place(relx=0.05, rely=0.72)
            get_priority = ttk.Combobox(frame, font = ('Montserrat', 25))
            font = tkFont.Font(family='Montserrat', size=18)
            frame.option_add("*TCombobox*Listbox*Font", font)
            get_priority['value'] = (
                'High', 'Medium', 'Low', 'Emergency', 'Redundant', 'Spontaneous', 'None')
            get_priority['state'] = ('readonly')
            get_priority.place(relx=0.3, rely=0.7, relwidth=0.6)

            # Database log:
            log = ttk.Button(frame, text='Enter')
            log.place(relx=0.75, rely=0.8, relwidth=0.15, relheight=0.05)
            log.bind('<Button>', get_input)

            # Return button:
            return_button = ttk.Button(frame, text='Return')
            return_button.place(relx=0.25, rely=0.8,
                                relwidth=0.15, relheight=0.05)
            return_button.bind('<Button>', return_action)

            # frame show:
            frame.pack(fill=BOTH, expand=True)
            input_clicked += 1

        # file output functions:
    def output_functions(event):
        global output_clicked
        global input_clicked
        global visualize
        #return button pressed
        def return_action(event):
            global output_clicked
            output_clicked = 0
            frame.destroy()
            welcome_frame.pack()

        #get output function if:
        if output_clicked == 0 and input_clicked == 0 and visualize == 0:
            # select directory:
            def dir_select(event):
                dir = filedialog.askdirectory()
                if len(dir) != 0:
                    os.chdir(dir)
                if len(dir_text.get()) == 0:
                    dir_text.insert(0, dir)
                elif len(dir_text.get()) != 0 and len(dir) != 0:
                    dir_text.delete(0, END)
                    dir_text.insert(0, dir)
            # file selection

            def file_action(event):
                file_select = filedialog.askopenfilename(filetypes=(
                    ("Excel(.xls)", "*.xls"), ("CSV(.csv)", "*.csv*")))
                if len(file_select) != 0 and len(file_entry.get()) != 0:
                    file_entry.delete(0, END)
                    file_entry.insert(0, file_select)
                elif len(file_entry.get()) == 0:
                    file_entry.insert(0, file_select)
            # save to csv:

            def csv_save(event):
                path = (dir_text.get()) + \
                    ('/USER_NO_{}'.format(str(target)) + ' Log File' + '.csv')
                database_get = mysql.connector.connect(
                    host='localhost', user='root', password='Haido29904', database='login_info')
                cursor_3 = database_get.cursor()
                try:
                    cursor_3.execute(
                        "SELECT * FROM login_info.USER_NO_{}".format(str(target)))
                    result = cursor_3.fetchall()
                finally:
                    database_get.close()
                # get column name ie: name, price,...
                column_names = list()
                # append all column names to result list
                for i in cursor_3.description:
                    column_names.append(i[0])
                result.append(column_names)
                # write to csv file:
                with open(path, 'w', newline='') as csv_file:
                    csvsave = csv.writer(
                        csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
                    for row in result:
                        csvsave.writerow(row)
                # open notification window
                messagebox.showinfo('Saved', 'File saved successfully!')

            # save to excel:
            def xls_save(event):
                path = (dir_text.get()) + \
                    '/USER_NO_{}'.format(str(target)) + ' Log File' + '.xls'
                database_get = mysql.connector.connect(
                    host='localhost', user='root', password='Haido29904', database='login_info')
                data_frame = pd.read_sql(
                    'SELECT * FROM login_info.USER_NO_{}'.format(target), database_get)
                data_frame.to_excel(path, index=False)
                messagebox.showinfo('Saved', 'File saved successfully!')

            # load to database
            def load_file(event):
                global target
                path = file_entry.get()
                if not path:
                    warning = messagebox.showwarning('File not found!')
                    warning.pack()
                else:
                    database = mysql.connector.connect(
                        host='localhost', user='root', password='Haido29904', database='login_info')
                    cursor_load = database.cursor()
                    cursor_load.execute(
                        "DROP TABLE IF EXISTS USER_NO_{}".format(str(target)))
                    cursor_load.execute(
                        "CREATE TABLE IF NOT EXISTS USER_NO_{}(id INTEGER PRIMARY KEY, name VARCHAR(255), price INTEGER, quantity INTEGER, tag VARCHAR(255))".format(str(target)))
                    insert = "INSERT into USER_NO_{}(id, name, price, quantity, tag) VALUES (%s, %s, %s, %s, %s)".format(
                        str(target))
                    if path.endswith('.csv'):
                        file = open(path)
                        csv_data = csv.reader(file)
                        for row in csv_data:
                            cursor_load.execute(insert, tuple(row))
                        database.commit()
                        cursor_load.close()
                        file.close()
                        database.close()
                    elif path.endswith('.xls'):
                        file_load = xlrd.open_workbook_xls(path)
                        excel_name = file_load.sheet_names()
                        sheet = file_load.sheet_by_name(excel_name[0])
                        for row in range(1, sheet.nrows):
                            id = sheet.cell(row, 0).value
                            name = sheet.cell(row, 1).value
                            price = sheet.cell(row, 2).value
                            quantity = sheet.cell(row, 3).value
                            tag = sheet.cell(row, 4).value
                            values = (id, name, price, quantity, tag)
                            cursor_load.execute(insert, tuple(values))
                            database.commit()
                        database.close()
                        cursor_load.close()
                    messagebox.showinfo(
                        "Congratulate!", "File loaded successfully!")

            # main output frame
            welcome_frame.pack_forget()
            frame = tk.Frame(root, background='#B1B2FF')
            # left bar:
            left = tk.Label(frame, background='#F29393')
            left.pack(side=LEFT, ipadx=10, ipady=1000)
            # right bar:
            right = tk.Label(frame, background='#F29393')
            right.pack(side=RIGHT, ipadx=10, ipady=1000)
            # top bar:
            top = tk.Label(frame, background='#F29393')
            top.pack(side=TOP, ipadx=1000, ipady=5)
            # bottom bar:
            bottom = tk.Label(frame, background='#F29393')
            bottom.pack(side=BOTTOM, ipadx=1000, ipady=5)
            # Title:
            title = ttk.Label(frame, text='Welcome to the file center', foreground='#ff6961', font=(
                'Broken Console', 25, 'bold'), background='#B1B2FF')
            title.config(anchor='center')
            title.place(relx=0.15, rely=0.1, relwidth=0.7)
            # Directory:
            dir = ttk.Button(frame, text='Choose \n directory')
            dir.place(relx=0.66, rely=0.24, relwidth=0.07, relheight=0.07)
            dir.bind('<Button>', dir_select)
            dir_text = ttk.Entry(frame)
            dir_text.place(relx=0.29, rely=0.25, relwidth=0.35, relheight=0.05)
            # Save to csv function;
            csv_button = ttk.Button(frame, text='Save to csv')
            csv_button.place(relx=0.3, rely=0.45, relwidth=0.1, relheight=0.1)
            csv_button.bind('<Button>', csv_save)
            # save to excel
            excel_button = ttk.Button(frame, text='Save to excel')
            excel_button.place(relx=0.6, rely=0.45,
                               relwidth=0.1, relheight=0.1)
            excel_button.bind('<Button>', xls_save)
            # select file entry and button
            file_select = ttk.Button(frame, text='Choose file \n (csv or xls)')
            file_select.place(relx=0.66, rely=0.65,
                              relwidth=0.075, relheight=0.07)
            file_select.bind('<Button>', file_action)
            file_entry = ttk.Entry(frame)
            file_entry.place(relx=0.29, rely=0.66,
                             relwidth=0.35, relheight=0.05)
            # load file
            load_func = ttk.Button(frame, text='Load file')
            load_func.place(relx=0.45, rely=0.75, relwidth=0.1, relheight=0.05)
            load_func.bind("<Button>", load_file)
            # return button functions:
            return_button = ttk.Button(frame, text='Return')
            return_button.place(relx=0.45, rely=0.85,
                                relwidth=0.1, relheight=0.05)
            return_button.bind('<Button>', return_action)
            # show frame:
            frame.pack(fill=BOTH, expand=True)
            output_clicked += 1

    #data visualization
    def get_visualization_frame(event):
        global input_clicked
        global output_clicked
        global visualize
        global target

        #return button function:
        def return_func(event):
            global visualize
            visualize = 0
            frame.destroy()
            welcome_frame.pack()
        
        #data visualization frame
        if input_clicked == 0 and output_clicked == 0 and visualize == 0:
            welcome_frame.pack_forget()
            frame = tk.Frame(root, background='#B1B2FF')

            #left bar:
            left = tk.Label(frame, background='#F29393')
            left.pack(side=LEFT, ipadx=10, ipady=1000)

            #right bar:
            right = ttk.Label(frame, background='#F29393')
            right.pack(side=RIGHT, ipadx=10, ipady=1000)

            #top bar:
            top = tk.Label(frame, background='#F29393')
            top.pack(side=TOP, ipadx=1000, ipady=5)

            #bottom bar:
            bottom = tk.Label(frame, background='#F29393')
            bottom.pack(side=BOTTOM, ipadx=1000, ipady=5)
            
            def graph_draw(event):
                global target
                database = mysql.connector.connect(host = 'localhost', user = 'root', password = 'Haido29904', database = 'login_info')
                cursor = database.cursor()
                if graph_info.get() == 'Retail Price':
                    cursor.execute("SELECT name, price FROM USER_NO_{}".format(str(target)))
                    result = cursor.fetchall()
                    name = []
                    price = []
                    for i in result:
                        name.append(i[0])
                        price.append(int(i[1]))
                    plt.figure(figsize=(12,6.75))
                    #label adding:
                    def add_labels():
                        for i in range(len(name)):
                            plt.text(i,price[i],price[i], ha = 'center')
                    #matplotlib plotting:
                    if graph_type.get() == 'Bar':
                        #bar graph:
                        plt.bar(name, price, color = ('#5B8899', '#FF1205' ,'#52D452'), width = 0.3)
                        plt.xlabel("Name of item")
                        plt.ylabel("Retail price of item")
                        plt.title('Retail price per item')
                        add_labels()
                        plt.show()

                        #line graph
                    elif graph_type.get() == 'Line':
                        #line graph:
                        plt.plot(name,price, color = ('#FF3D33'))
                        plt.xlabel("Name of item")
                        plt.ylabel("Price of item")
                        plt.title('Retail price per item')
                        add_labels()
                        plt.show()

                    elif graph_type.get() == 'Pie':
                        wedge = {"linewidth":1, "edgecolor":"black"}
                        plt.pie(price, radius = 1, startangle = 90, wedgeprops=wedge, autopct= '%1.1f%%')
                        plt.title('Retail price per item')
                        plt.legend(title = 'Name of item', loc = "upper right", labels = name, bbox_to_anchor = (1.15,0.65))
                        plt.show()

                elif graph_info.get() == 'Quantity':
                    cursor.execute("SELECT name, quantity FROM USER_NO_{}".format(str(target)))
                    result = cursor.fetchall()
                    name = []
                    quantity = []
                    plt.figure(figsize = (12, 6.75))
                    for i in result:
                        name.append(i[0])
                        quantity.append(i[1])
                    def add_label():
                        for i in range(len(name)):
                            plt.text(i, quantity[i], quantity[i], ha ='center')
                    if graph_type.get() == 'Bar':
                        #Bar graph
                        plt.bar(name, quantity, color = ('#5B8899', '#FF1205' ,'#52D452'), width = 0.3)
                        plt.title('Quantity per category')
                        plt.xlabel('Name of item')
                        plt.ylabel('Quantity of item')
                        add_label()
                        plt.show()

                    elif graph_type.get() == 'Line':
                        #Line graph:
                        plt.plot(name, quantity, color = '#FF3D33')
                        plt.title('Quantity per category')
                        plt.xlabel('Name of item')
                        plt.ylabel('Quantity of item')
                        add_label()
                        plt.show()

                    elif graph_type.get() == 'Pie':
                        #Pie graph:
                        wedge = {"linewidth":1, "edgecolor":"black"}
                        def make_autopct(quantity):
                            def autopct_maker(pct):
                                total = sum(quantity)
                                val = int(round(pct*total/100.0))
                                return '{p:.1f}% ({v:d})'.format(p = pct, v = val)
                            return autopct_maker
                        plt.pie(quantity, radius = 1, startangle=90, wedgeprops=wedge, autopct= make_autopct(quantity))
                        plt.title('Quantity per category')
                        plt.legend(title = 'Name of item', loc = 'upper right', labels = name, bbox_to_anchor = (1.15, 0.65))
                        plt.show()

                elif graph_info.get() == 'Total Value':
                    #Total value graph:
                    plt.figure(figsize=(12,6.75))
                    cursor.execute("SELECT name, total_value FROM USER_NO_{}".format(str(target)))
                    result = cursor.fetchall()
                    name = []
                    total_value = []
                    for i in result:
                        name.append(i[0])
                        total_value.append(i[1])
                    def add_value():
                        for i in range(len(name)):
                            plt.text(i, total_value[i], total_value[i], ha = 'center')
                    #Bar graph:
                    if graph_type.get() == 'Bar':
                        plt.bar(name,total_value, width=0.3, color = ('#5B8899', '#FF1205' ,'#52D452'))
                        plt.title('Total value per item')
                        plt.xlabel('Name of item')
                        plt.ylabel('Total value of item')
                        add_value()
                        plt.show()
                    
                    #line graph:
                    elif graph_type.get() == 'Line':
                        plt.plot(name, total_value,color = '#FF3D33')
                        plt.title('Total value per item')
                        plt.xlabel('Name of item')
                        plt.ylabel('Total value of item')
                        add_value()
                        plt.show()

                    #pie graph:
                    elif graph_type.get() == 'Pie':
                        wedge = {"linewidth":1, "edgecolor":"black"}
                        def make_autopct(total_value):
                            def autopct_maker(pct):
                                total = sum(total_value)
                                val = int(round(pct*total/100.0))
                                return '{p:.1f}% ({v:d})'.format(p = pct, v = val)
                            return autopct_maker
                        plt.pie(total_value, radius = 1, startangle = 90, wedgeprops = wedge, autopct = make_autopct(total_value))
                        plt.legend(name, loc = "upper right", bbox_to_anchor = (1.15,0.65))
                        plt.title('Total value per item')
                        plt.show()
                
                elif graph_info.get() == 'All':
                    cursor.execute("SELECT name, price,")
            #Graphing:
            graph_text = ttk.Label(frame, text = 'Choose a attribute to display',foreground = '#4169e1', background = '#B1B2FF', font = ('Broken Console', 18))
            graph_text.config(anchor = CENTER)
            graph_text.place(relx = 0.03, rely = 0.15, relwidth = 0.945, relheight = 0.08)
            graph_info = ttk.Combobox(frame, font =('Montserrat', 15))
            font = tkFont.Font(family='Montserrat', size=15)
            frame.option_add("*TCombobox*Listbox*Font", font)
            graph_info.place(relx = 0.43, rely = 0.25, relwidth = 0.15, relheight = 0.06)
            graph_info['value'] = ('Retail Price', 'Quantity', 'Total Value', 'All')
            graph_info['state'] = ['readonly']

            #Graph type:
            graph_type_text = ttk.Label(frame, text = 'Choose a type of graph to display', foreground = '#4169e1', background = '#B1B2FF', font = ('Broken Console', 18))
            graph_type_text.config(anchor = CENTER)
            graph_type_text.place(relx = 0.03, rely = 0.4, relwidth = 0.945, relheight = 0.08)
            graph_type = ttk.Combobox(frame,font =('Montserrat', 15))
            graph_type.place(relx = 0.43, rely = 0.5, relwidth = 0.15, relheight = 0.06)
            graph_type['value'] = ('Bar', 'Line', 'Pie')
            graph_type['state'] = ['readonly']

            #Create graph button:
            graph = ttk.Button(frame, text = 'Start Graphing')
            graph.place(relx = 0.62, rely = 0.7, relwidth = 0.15, relheight = 0.08)
            graph.bind('<Button>', graph_draw)
            #return button:
            return_button = ttk.Button(frame, text='Return')
            return_button.place(relx = 0.25, rely = 0.7, relwidth =0.15, relheight = 0.08)
            return_button.bind('<Button>', return_func)
            
            #frame show
            frame.pack(fill=BOTH, expand=True)
            visualize += 1

    #exit function
    def exit_app(event):
        root.destroy()
        sys.exit(0)

        # hover to change color(WHY TF did I write this :)) I should have written this as class No code reusable here)
    def input_appearance(event):
        input_data.config(background='#FFB2A6')
    def input_deappearance(event):
        input_data.config(background='#FF8AAE')

    def output_appearance(event):
        output_data.config(background='#FFB2A6')
    def output_deappearance(event):
        output_data.config(background='#FF8AAE')

    def graph_data_appearance(event):
        graph_data.config(background='#FFB2A6')
    def graph_data_deappearance(event):
        graph_data.config(background='#FF8AAE')

    def log_out_appearance(event):
        log_out.config(background='#FFB2A6')
    def log_out_deappearance(event):
        log_out.config(background='#FF8AAE')

    def input_icon_label_appearance(event):
        input_icon_label.config(background='#A9A9A9')
    def input_icon_label_deappearance(event):
        input_icon_label.config(background='#9E74D0')

    def center_icon_label_appearance(event):
        center_icon_label.config(background='#A9A9A9')
    def center_icon_label_deappearance(event):
        center_icon_label.config(background='#9E74D0')
    
    def bar_icon_label_appearance(event):
        bar_icon_label.config(background='#A9A9A9')
    def bar_icon_label_deappearance(event):
        bar_icon_label.config(background='#9E74D0')
    
    def exit_icon_label_appearance(event):
        exit_icon_label.config(background='#A9A9A9')
    def exit_icon_label_deappearance(event):
        exit_icon_label.config(background='#9E74D0')

    def update_data_appearance(event):
        update_data.config(background = '#FFB2A6')
    def update_data_deappearance(event):
        update_data.config(background='#FF8AAE')

    def update_icon_appearance(event):
        update_icon_label.config(background='#A9A9A9')
    def update_icon_deappearance(event):
        update_icon_label.config(background='#9E74D0')
    # Dashboard main windows
    root = tk.Tk()
    root.geometry("1280x720+300+150")
    root.title("Financial Dashboard")
    root.resizable(0, 0)

    label = ttk.Label(root, text='Financial Dashboard', font=(
        'Broken Console', 30, 'bold'), background='#BE3EBE', foreground='#00FFFF')
    label.pack(ipady=10, fill=tk.X)
    label.config(anchor=CENTER)

    menu = ttk.Label(root, background='#9E74D0')
    menu.pack(side=LEFT, ipadx=150, fill=tk.Y)

    icon = ImageTk.PhotoImage(Image.open(
        'C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\Menu icon.png'))
    menu_icon = tk.Label(root, image=icon, background='#9E74D0')
    menu_icon.place(x=260, y=73)
    menu_icon.bind('<Button>', menu_entry)

    #create welcome frame
    welcome_frame = tk.Frame(background = '#B1B2FF')

    #left bar:
    left = tk.Label(welcome_frame, background='#F29393')
    left.pack(side=LEFT, ipadx=10, ipady=1000)
    # right bar:
    right = ttk.Label(welcome_frame, background='#F29393')
    right.pack(side=RIGHT, ipadx=10, ipady=1000)
    # top bar:
    top = tk.Label(welcome_frame, background='#F29393')
    top.pack(side=TOP, ipadx=1000, ipady=5)
    # bottom bar:
    bottom = tk.Label(welcome_frame, background='#F29393')
    bottom.pack(side=BOTTOM, ipadx=1000, ipady=5)

    #Welcome bar:
    welcome = ttk.Label(welcome_frame, text ='Welcome to the Financial Dashboard', background='#B1B2FF', font = ('Broken Console', 25, 'bold'), foreground='#201E1F')
    welcome.config(anchor = CENTER)
    welcome.place(relx = 0.026, rely = 0.1, relwidth=0.945, relheight=0.1)

    #Instruction:
    instruction = ttk.Label(welcome_frame, text ='About Financial Dashboard', background='#B1B2FF', font = ('Broken Console', 17, 'bold'), foreground='#ff6961')
    instruction.config(anchor = CENTER)
    instruction.place(relx = 0.3, rely = 0.2)

    #Instruction text:
    instruction_text = ttk.Label(welcome_frame, text ='This app was created with the intention of helping students \n          and/or those who have minimum financial budget', background='#B1B2FF', font = ('Broken Console', 13, 'bold'))
    instruction_text.config(anchor = CENTER)
    instruction_text.place(relx = 0.026, rely = 0.3, relwidth=0.945)

    #about author:
    author = ttk.Label(welcome_frame, text = 'About Author', background = '#B1B2FF', font = ('Broken Console', 17, 'bold'), foreground = '#ff6961')
    author.config(anchor = CENTER)
    author.place(relx = 0.37, rely = 0.4)

    #Facebook button:

    #Link function:
    def facebook_link(event):
        webbrowser.open('https://www.facebook.com/profile.php?id=100009265639926')

    #Hover to change color:
    def facebook_appearance(event):
        facebook.config(background='#00008B')
        facebook_icon_label.config(background='#00008B')
    def facebook_deappearance(event):
        facebook.config(background='#4267B2')
        facebook_icon_label.config(background='#4267B2')
    facebook = tk.Label(welcome_frame, text ='Facebook', background='#4267B2', font = ('Segoe UI', 13, 'bold'), borderwidth = 2, relief = "solid")
    facebook.config(anchor = CENTER)
    facebook.place(relx = 0.1, rely = 0.5, relwidth=0.135   , relheight = 0.08)
    facebook.bind('<Button>', facebook_link)
    facebook.bind('<Enter>', facebook_appearance)
    facebook.bind('<Leave>', facebook_deappearance)
    facebook_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\facebook.png'))
    facebook_icon_label = tk.Label(facebook, image=facebook_icon, background='#4267B2')
    facebook_icon_label.place(relx = 0, rely = 0.24)
    facebook_icon_label.bind('<Button>', facebook_link)

    #Github button:
    #Link function:
    def github_link(event):
        webbrowser.open('https://github.com/Sunflowerformylove')

    #Hover to change color:
    def github_appearance(event):
        github.config(background = 'white', foreground = '#2E2E2E')
        github_icon_label.config(background = 'white')
    def github_deappearance(event):
        github.config(background = '#2E2E2E', foreground = 'white')
        github_icon_label.config(background = '#2E2E2E')
    github = tk.Label(welcome_frame, text ='Github', background='#2E2E2E', foreground ='white', font = ('Segoe UI', 14, 'bold'), borderwidth = 2, relief = "solid")
    github.config(anchor = CENTER)
    github.place(relx = 0.41, rely = 0.5, relwidth=0.135, relheight=0.08)
    github.bind('<Button>', github_link)
    github.bind('<Enter>', github_appearance)
    github.bind('<Leave>', github_deappearance)
    github_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\github.png'))
    github_icon_label = tk.Label(github, image = github_icon, background = '#2E2E2E')
    github_icon_label.place(relx = 0, rely = 0.15)
    github_icon_label.bind('<Button>', github_link)

    #Instagram button:
    #Link function:
    def instagram_link(event):
        webbrowser.open('https://www.instagram.com/sea_pea_04/')
    #Hover to change color:
    def instagram_appearance(event):
        instagram.config(background='#F56040')
        instagram_icon_label.config(background = '#F56040')
    def instagram_deappearance(event):
        instagram.config(background='#FD1D1D')
        instagram_icon_label.config(background = '#FD1D1D')
    instagram = tk.Label(welcome_frame, text ='Instagram', background='#FD1D1D', font = ('Segoe UI', 13, 'bold'), borderwidth = 2, relief = "solid")
    instagram.config(anchor = CENTER)
    instagram.bind('<Button>', instagram_link)
    instagram.bind('<Enter>', instagram_appearance)
    instagram.bind('<Leave>', instagram_deappearance)
    instagram.place(relx = 0.71, rely = 0.5, relwidth=0.135, relheight=0.08)
    instagram_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\instagram.png'))
    instagram_icon_label = tk.Label(instagram, image = instagram_icon, background='#FD1D1D')
    instagram_icon_label.place(relx = 0, rely = 0.24)

    #Last say
    say = ttk.Label(welcome_frame, text = 'FROM DO HAI WITH LUV!', font = ('Broken Console', 22, 'bold'), background='#B1B2FF', foreground = '#E48CA3')
    say.config(anchor = CENTER)
    say.place(relx = 0.027, rely = 0.7, relheight=0.1, relwidth = 0.948)
    heart_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\heart.png'))
    heart = tk.Label(say, image=heart_icon, background='#B1B2FF')
    heart.place(relx = 0.72, rely = 0)
    #frame show
    welcome_frame.pack(fill = BOTH, expand = True)

    input_data = ttk.Label(root, text='Add Items', background='#FF8AAE', font=(
        'Oddly Calming', 15, 'bold'))
    input_data.place(x=0, y=110, height=60, width=304)
    input_data.config(anchor=CENTER)
    input_data.bind('<Enter>', input_appearance)
    input_data.bind('<Leave>', input_deappearance)
    input_data.bind('<Button>', input_functions)

    update_data = ttk.Label(root, text ='Update Items',  background='#FF8AAE', font=(
        'Oddly Calming', 15, 'bold'))
    update_data.config(anchor=CENTER)
    update_data.place(x=0, y=240, height=60, width=304)
    update_data.bind('<Enter>', update_data_appearance)
    update_data.bind('<Leave>', update_data_deappearance)
    update_data.bind('<Button>')

    output_data = ttk.Label(root, text='File Center', background='#FF8AAE', font=(
        'Oddly Calming', 15, 'bold'))
    output_data.place(x=0, y=380, height=60, width=304)
    output_data.config(anchor=CENTER)
    output_data.bind('<Enter>', output_appearance)
    output_data.bind('<Leave>', output_deappearance)
    output_data.bind('<Button>', output_functions)

    graph_data = ttk.Label(root, text='Data Visualization', background='#FF8AAE', font=(
        'Oddly Calming', 15, 'bold'))
    graph_data.place(x=0, y=520, width=304, height=60)
    graph_data.config(anchor=CENTER)
    graph_data.bind('<Enter>', graph_data_appearance)
    graph_data.bind('<Leave>', graph_data_deappearance)
    graph_data.bind('<Button>', get_visualization_frame)

    log_out = ttk.Label(root, text = 'Log Out', background = '#FF8AAE', font = ('Oddly Calming', 15,' bold'))
    log_out.config(anchor=CENTER)
    log_out.place(x=0, y=650, width=304, height=60)
    log_out.bind('<Enter>', log_out_appearance)
    log_out.bind('<Leave>', log_out_deappearance)
    log_out.bind('<Button>', exit_app)    

    input_icon = ImageTk.PhotoImage(Image.open(
        'C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\Input.png'))
    input_icon_label = tk.Label(root, image=input_icon, background='#9E74D0')
    input_icon_label.bind('<Button>', input_functions)
    input_icon_label.bind('<Enter>', input_icon_label_appearance)
    input_icon_label.bind('<Leave>', input_icon_label_deappearance)

    center_icon = ImageTk.PhotoImage(Image.open(
        'C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\centre.png'))
    center_icon_label = tk.Label(root, image=center_icon, background='#9E74D0')
    center_icon_label.bind('<Button>', output_functions)
    center_icon_label.bind('<Enter>', center_icon_label_appearance)
    center_icon_label.bind('<Leave>', center_icon_label_deappearance)

    bar_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\bar.png'))
    bar_icon_label = tk.Label(root, image=bar_icon, background='#9E74D0')
    bar_icon_label.bind('<Enter>', bar_icon_label_appearance)
    bar_icon_label.bind('<Leave>', bar_icon_label_deappearance)
    bar_icon_label.bind('<Button>', get_visualization_frame)

    exit_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\exit.png'))
    exit_icon_label = tk.Label(root, image=exit_icon, background='#9E74D0')
    exit_icon_label.bind('<Enter>', exit_icon_label_appearance)
    exit_icon_label.bind('<Leave>', exit_icon_label_deappearance)
    exit_icon_label.bind('<Button>', exit_app)

    update_icon = ImageTk.PhotoImage(Image.open('C:\\Users\\dodin\\Desktop\\Workplace\\Python project\\Financial Dashboard\\update.png'))
    update_icon_label = tk.Label(root, image = update_icon, background='#9E74D0')
    update_icon_label.bind('<Enter>', update_icon_appearance)
    update_icon_label.bind('<Leave>', update_icon_deappearance)
    update_icon_label.bind('<Button>')
    root.mainloop()

try:
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    login_screen()
