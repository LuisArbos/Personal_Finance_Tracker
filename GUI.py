from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import tkinterDnD
from datetime import datetime

data = []
appearance_mode_mapping = {
    "English": {
        "Claro": "Light",
        "Oscuro": "Dark",
        "Sistema": "System",
        "Light": "Light",
        "Dark": "Dark",
        "System": "System"
    },
    "Spanish": {
        "Light": "Claro",
        "Dark": "Oscuro",
        "System": "Sistema",
        "Claro": "Claro",
        "Oscuro": "Oscuro",
        "Sistema": "Sistema"
    }
}

translations = {
    "English": {
        "title": "Personal Finance Tracker",
        "title2": "Personal Finance \rTracker",
        "add_income": "Add Income",
        "add_expense": "Add Expense",
        "upload": "Upload data",
        "export": "Export data",
        "no_history": "There is no history data. Please add some data.",
        "history": "Transaction History",
        "appearance_mode": "Appearance Mode:",
        "values": ["Light", "Dark", "System"],
        "languages": ["English", "Spanish"],
        "language": "Language:",
        "dialog_event": "Type in a number:",
        "column_titles": ["Type",  "Amount", "Date", "Category"]
    },
    "Spanish": {
        "title": "Rastreador de Finanzas Personales",
        "title2": "Rastreador de \rFinanzas Personales",
        "add_income": "Añadir Ingreso",
        "add_expense": "Añadir Gasto",
        "upload": "Cargar datos",
        "export": "Exportar datos",
        "no_history": "No hay datos históricos. Por favor, añada algun dato.",
        "history": "Historial de transacciones",
        "appearance_mode": "Apariencia:",
        "values": ["Claro", "Oscuro", "Sistema"],
        "languages": ["Inglés", "Español"],
        "language": "Idioma:",
        "dialog_event": "Añade un número:",
        "column_titles": ["Tipo",  "Cantidad", "Fecha", "Categoría"]
    }

}

ctk.set_ctk_parent_class(tkinterDnD.Tk)
ctk.set_appearance_mode("System")    #Pending to add a button to choose dark or light theme
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800")
        self.language = "English"
        self.title(translations[self.language]["title"])

        #Create a grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #Side Bar Frame
        self.sidebar_frame = ctk.CTkFrame(master=self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        #Side Bar Additions
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Personal Finance \r Tracker", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button_income = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["add_income"], command=lambda:self.open_input_dialog_event(translations[self.language]["add_income"]))
        self.button_income.grid(row=1, column = 0, padx=10, pady=10)
        self.button_expense = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["add_expense"], command=lambda:self.open_input_dialog_event(translations[self.language]["add_expense"]))
        self.button_expense.grid(row=2, column = 0, padx=10, pady=10)
        self.button_upload = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["upload"], command=self.upload_file)
        self.button_upload.grid(row=3, column = 0, padx=10, pady=10)
        self.button_export = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["export"], command=self.export_file)
        self.button_export.grid(row=4, column = 0, padx=10, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(master=self.sidebar_frame, text=translations[self.language]["appearance_mode"], anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearence_mode_list = ctk.CTkOptionMenu(master=self.sidebar_frame, values=translations[self.language]["values"], command=self.change_appearance_mode_event)
        self.appearence_mode_list.grid(row=7, column=0, padx=20, pady=(0, 10))
        self.language_mode_list = ctk.CTkOptionMenu(master=self.sidebar_frame, values=translations[self.language]["languages"], command=self.change_language)
        self.language_mode_list.grid(row=8, column=0, padx=20, pady=(5, 20))
        
        #Graphs Frame
        self.graphs_frame = ctk.CTkFrame(master=self)
        self.graphs_frame.grid(row=0, column=1, columnspan=3, sticky="nsew")

        #History Frame
        self.history_frame = ctk.CTkFrame(master=self)
        self.history_frame.grid(row=1, column=1, columnspan=3, rowspan=3, sticky="nsew")

        self.appearence_mode_list.set("Dark")
        self.language_mode_list.set(self.language)
        self.refresh_data()
    #Functions
    def change_appearance_mode_event(self, new_appearance_mode: str):
        if self.language == "Spanish" or self.language == "Español":
            if new_appearance_mode == "Claro":
                translated_mode = "Light"
            elif new_appearance_mode == "Oscuro":
                translated_mode = "Dark"
            elif new_appearance_mode == "Sistema":
                translated_mode = "System"
        else:
            translated_mode = new_appearance_mode
        
        ctk.set_appearance_mode(translated_mode)
        
        self.refresh_data()
        
    def open_input_dialog_event(self, title):
        dialog = ctk.CTkInputDialog(text=translations[self.language]["dialog_event"], title=title)
        quantity = float(dialog.get_input())
        category_dialog = ctk.CTkInputDialog(text="Enter category:", title="Category")
        category = category_dialog.get_input()
        date = datetime.now().strftime("%Y-%m-%d")
        if title == translations[self.language]["add_income"]:
            movement_type = "Income" 
        else:
            movement_type = "Expense"
        data.append({"type": movement_type, "amount": quantity, "date": date, "category": category})
        self.refresh_data()

    def change_language(self, language):
        print("Switching laguange to: ", language)
        if language == "Inglés":
            language = "English" 
        elif language == "Español":
            language = "Spanish"
        self.language = language
        self.title(translations[language]["title"])
        self.button_income.configure(text=translations[language]["add_income"])
        self.button_expense.configure(text=translations[language]["add_expense"])
        self.button_upload.configure(text=translations[language]["upload"])
        self.button_export.configure(text=translations[language]["export"])
        self.appearance_mode_label.configure(text=translations[language]["appearance_mode"])
        self.appearence_mode_list.configure(values=translations[language]["values"])
        self.language_mode_list.configure(values=translations[language]["languages"])
        
        current_mode_to_set = appearance_mode_mapping[language][self.appearence_mode_list.get()]
        self.appearence_mode_list.set(current_mode_to_set)
        self.language_mode_list.set("Español") if language == "Spanish" else self.language_mode_list.set("English")
        #self.language_mode_list.set(language)
        self.refresh_data()
        
    def upload_file(self):
        print("Uploading file!")

    def export_file(self):
        print("Export file!")

    def refresh_data(self):
        #for widget in self.history_frame.winfo_children():
            #widget.destroy()
        column_titles = translations[self.language]["column_titles"]
        if not data:
            self.history_non_label = ctk.CTkLabel(master=self.history_frame, text=translations[self.language]["no_history"])
            self.history_non_label.grid(row=1, column=1, padx=20, pady=20)
        else:
            self.history_scrollable_frame = ctk.CTkScrollableFrame(master=self, label_text=translations[self.language]["history"])
            self.history_scrollable_frame.grid(row=1, column=1, columnspan=3, rowspan=3, sticky="nsew")
            for idx, title in enumerate(column_titles):
                title_label = ctk.CTkLabel(self.history_scrollable_frame, text=title, font=ctk.CTkFont(size=12, weight="bold"))
                title_label.grid(row=2, column=idx, padx=10, pady=5)

            for idx, entry in enumerate(data):
                type_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{entry['type']}")
                type_label.grid(row=idx+3, column=0, padx=10, pady=5)
                amount_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{entry['amount']}")
                amount_label.grid(row=idx+3, column=1, padx=10, pady=5)
                date_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{entry['date']}")
                date_label.grid(row=idx+3, column=2, padx=10, pady=5)
                category_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{entry.get('category', 'N/A')}")
                category_label.grid(row=idx+3, column=3, padx=10, pady=5)

app= App()
app.mainloop()