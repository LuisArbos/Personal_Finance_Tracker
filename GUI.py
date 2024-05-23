from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import tkinterDnD

colors = ['#585E69', '#616773', '#6B717E', '#A0A7A6', '#BAC2BA', '#D4DCCD', '#D8DFD2']


ctk.set_ctk_parent_class(tkinterDnD.Tk)
ctk.set_appearance_mode("System")    #Pending to add a button to choose dark or light theme
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800")
        self.title("Personal Finance Tracker")

        #Create a grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #Side Bar Frame
        self.sidebar_frame = ctk.CTkFrame(master=self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        #Main Frame
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.grid(row=0, column=1, columnspan=3, rowspan=4, sticky="nsew")
        #self.main_frame.grid_rowconfigure(4, weight=1)

        #self.main_frame.pack(pady=20, padx=20, fill="both", expand = True)


        
        #First Label
        label_1 = ctk.CTkLabel(master=self.main_frame, font=ctk.CTkFont(size=20, weight="bold"), text="Hi! What would you like to do?", justify="center")
        label_1.grid(row=0, column=0, padx=10, pady=10)

        #Buttons
        button_1 = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text= "Button 1")
        button_2 = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text= "Button 2")
        button_3 = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text= "Button 3")
        button_1.grid(row=0, pady=10, padx=10)
        button_2.grid(row=1, pady=10, padx=10)
        button_3.grid(row=2, pady=10, padx=10)

"""
Label(main_frame, text="Income:", bg=colors[4]).grid(row=0, column=0, sticky=W)
income_entry = Entry(main_frame)
income_entry.config(bg=colors[4])
income_entry.grid(row=0, column=1, sticky=(W, E))

Label(main_frame, text="Expenses:", bg=colors[4]).grid(row=1, column=0, sticky=W)
expenses_entry = Entry(main_frame)
expenses_entry.config(bg=colors[4])
expenses_entry.grid(row=1, column=1, sticky=(W, E))

def calculate_balance():
    income = float(income_entry.get())
    expenses = float(expenses_entry.get())
    balance = income - expenses
    result_label.config(text=f"Balance: ${balance:.2f}")

calculate_button = ctk.CTkButton(master=main_frame, corner_radius= 10, text="Calculate Balance", command=calculate_balance)
calculate_button.grid(row=2, column=2, columnspan=2)

result_label = Label(main_frame, text="Balance: $0.00")
result_label.grid(row=3, column=3, columnspan=2)"""


app= App()
app.mainloop()