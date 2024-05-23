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
        
        #Side Bar Additions
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Personal Finance \rTracker", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button_income = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text= "Add income", command=lambda:self.open_input_dialog_event("Add income"))
        self.button_income.grid(row=1, column = 0, padx=10, pady=10)
        self.button_expense = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text= "Add expense", command=lambda:self.open_input_dialog_event("Add expense"))
        self.button_expense.grid(row=2, column = 0, padx=10, pady=10)
        self.button_history = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text= "Check movements")
        self.button_history.grid(row=3, column = 0, padx=10, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(master=self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearence_mode_list = ctk.CTkOptionMenu(master=self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearence_mode_list.grid(row=6, column=0, padx=20, pady=(10, 20))
        
        #Main Frame
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.grid(row=0, column=1, columnspan=3, rowspan=4, sticky="nsew")
        #self.main_frame.grid_rowconfigure(4, weight=1)

        #self.main_frame.pack(pady=20, padx=20, fill="both", expand = True)


        self.appearence_mode_list.set("Dark")
    #Functions
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def open_input_dialog_event(self, title):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title=title)
        print("Input Dialog:", dialog.get_input())
        



app= App()
app.mainloop()