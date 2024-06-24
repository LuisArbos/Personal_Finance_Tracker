from tkinter import *
import customtkinter as ctk
from tkcalendar import Calendar
import tkinterDnD
from datetime import datetime, timedelta
import pandas as pd

import csv, os, shutil

import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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
        "dialog_event2": "Select a category (max. 1)",
        "dialog_event3": "Add a comment:",
        "column_titles": ["Type",  "Amount", "Date", "Category", "Comment"],
        "upload_title": "Select a File",
        "export_title": "Save as",
        "graph_title": "Income/Expense Graphic",
        "income_categories": ["Salary", "Other"],
        "expense_categories": ["House","Services", "Food", "Entertainment", "Other"],
        "filter_title": "Filters",
        "graph_title": "Income and Expenses",
        "graph_amount": "Amount",
        "graph_category": "Category",
        "apply": "Apply",
        "Type": "Type"
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
        "dialog_event2": "Selecciona una categoria (max. 1)",
        "dialog_event3": "Añade un comentario:",
        "column_titles": ["Tipo",  "Cantidad", "Fecha", "Categoría", "Comentario"],
        "upload_title": "Selecciona un archivo",
        "export_title": "Guardar como",
        "graph_title": " Gráfico de Ingresos y Gastos",
        "income_categories": ["Sueldo", "Otros"],
        "expense_categories": ["Casa", "Servicios", "Comida", "Ocio", "Otros"],
        "filter_title": "Filtros",
        "graph_title": "Ingresos y Gastos",
        "graph_amount": "Cantidad",
        "graph_category": "Categoría",
        "apply": "Aplicar",
        "Salary": "Sueldo",
        "Other": "Otros",
        "House": "Casa",
        "Services": "Servicios",
        "Food": "Comida",
        "Entertainment": "Ocio",
        "Type": "Tipo",
        "Income": "Ingreso",
        "Expense": "Gasto"
    }

}

ctk.set_ctk_parent_class(tkinterDnD.Tk)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x800")
        self.language = "English"
        self.path = "data.csv"
        self.title(translations[self.language]["title"])
        self.light_mode = 'Dark'
        self.current_switch_var_on = ["Salary", "House","Services", "Food", "Entertainment", "Other"]
        #Create a grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #Side Bar Section
        self.sidebar_frame = ctk.CTkFrame(master=self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        #Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Personal Finance \r Tracker", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #Buttons
        self.button_income = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["add_income"], command=lambda:self.open_input_dialog_event(translations[self.language]["add_income"]))
        self.button_income.grid(row=1, column = 0, padx=10, pady=10)
        self.button_expense = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["add_expense"], command=lambda:self.open_input_dialog_event(translations[self.language]["add_expense"]))
        self.button_expense.grid(row=2, column = 0, padx=10, pady=10)
        self.button_upload = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["upload"], command=self.upload_file)
        self.button_upload.grid(row=3, column = 0, padx=10, pady=10)
        self.button_export = ctk.CTkButton(master=self.sidebar_frame, corner_radius=10, text_color = "black", text=translations[self.language]["export"], command=self.export_file)
        self.button_export.grid(row=4, column = 0, padx=10, pady=10)

        #Additional features
        self.appearance_mode_label = ctk.CTkLabel(master=self.sidebar_frame, text=translations[self.language]["appearance_mode"], anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearence_mode_list = ctk.CTkOptionMenu(master=self.sidebar_frame, values=translations[self.language]["values"], command=self.change_appearance_mode_event)
        self.appearence_mode_list.grid(row=7, column=0, padx=20, pady=(0, 10))
        self.language_mode_list = ctk.CTkOptionMenu(master=self.sidebar_frame, values=translations[self.language]["languages"], command=self.change_language)
        self.language_mode_list.grid(row=8, column=0, padx=20, pady=(5, 20))
        
        #Graphs Frame
        self.graphs_frame = ctk.CTkFrame(master=self)        
        self.graphs_right_frame = ctk.CTkFrame(master=self)

        #History Frame
        self.history_frame = ctk.CTkFrame(master=self)        

        #Filter Section
        self.filter_frame = ctk.CTkFrame(master=self)
        self.filter_title = ctk.CTkLabel(master=self.filter_frame, text=translations[self.language]["filter_title"], font=ctk.CTkFont(size=16, weight="bold"))
        
        self.calendar_start_date = ctk.CTkEntry(master=self.filter_frame)
        self.calendar_start_date.insert(0, (datetime.now() - timedelta(days=365)).strftime("%d-%m-%Y"))
        self.calendar_start_date_button = ctk.CTkButton(master=self.filter_frame, text="Select Date", command=lambda:self.open_calendar(self.calendar_start_date))
        self.calendar_end_date = ctk.CTkEntry(master=self.filter_frame)
        self.calendar_end_date.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.calendar_end_date_button = ctk.CTkButton(master=self.filter_frame, text="Select Date", command=lambda:self.open_calendar(self.calendar_end_date))
        self.switch_var_list = [StringVar(value="on"), StringVar(value="on"), StringVar(value="on"), StringVar(value="on"), StringVar(value="on"), StringVar(value="on")]
        self.switch_1 = ctk.CTkSwitch(master=self.filter_frame, text=translations[self.language]["income_categories"][0],  variable=self.switch_var_list[0], onvalue="on", offvalue="off")
        self.switch_2 = ctk.CTkSwitch(master=self.filter_frame, text=translations[self.language]["expense_categories"][0], variable=self.switch_var_list[1], onvalue="on", offvalue="off")
        self.switch_3 = ctk.CTkSwitch(master=self.filter_frame, text=translations[self.language]["expense_categories"][1], variable=self.switch_var_list[2], onvalue="on", offvalue="off")
        self.switch_4 = ctk.CTkSwitch(master=self.filter_frame, text=translations[self.language]["expense_categories"][2], variable=self.switch_var_list[3], onvalue="on", offvalue="off")
        self.switch_5 = ctk.CTkSwitch(master=self.filter_frame, text=translations[self.language]["expense_categories"][3], variable=self.switch_var_list[4], onvalue="on", offvalue="off")
        self.switch_6 = ctk.CTkSwitch(master=self.filter_frame, text=translations[self.language]["expense_categories"][4], variable=self.switch_var_list[5], onvalue="on", offvalue="off")
        self.filter_button = ctk.CTkButton(master=self.filter_frame, corner_radius=10, text_color = "black", text=translations[self.language]["apply"], command=self.apply_filter)
        
        #Setting default values
        self.appearence_mode_list.set("Dark")
        self.language_mode_list.set(self.language)
        self.refresh_data()
    

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
        self.light_mode = translated_mode
        ctk.set_appearance_mode(translated_mode)
        
        self.refresh_data()
        
    def open_input_dialog_event(self, title):
        if self.input_dialog_window is None or self.input_dialog_window.winfo_exists():
            self.input_dialog_window = TopLevelWindow(self, title)
        else:
            self.input_dialog_window.lift()
            self.input_dialog_window.focus_force()

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
        self.filter_title.configure(text=translations[self.language]["filter_title"])
        self.switch_1.configure(text=translations[self.language]["income_categories"][0])
        self.switch_2.configure(text=translations[self.language]["expense_categories"][0])
        self.switch_3.configure(text=translations[self.language]["expense_categories"][1])
        self.switch_4.configure(text=translations[self.language]["expense_categories"][2])
        self.switch_5.configure(text=translations[self.language]["expense_categories"][3])
        self.switch_6.configure(text=translations[self.language]["expense_categories"][4])
        
        current_mode_to_set = appearance_mode_mapping[language][self.appearence_mode_list.get()]
        self.appearence_mode_list.set(current_mode_to_set)
        self.language_mode_list.set("Español") if language == "Spanish" else self.language_mode_list.set("English")

        self.refresh_data()

    def open_calendar(self, entry):
        def select_date():
            date = cal.selection_get()
            entry.delete(0, ctk.END)
            entry.insert(0, date.strftime("%d-%m-%Y"))
            top.destroy()
        
        top = ctk.CTkToplevel(master=self)
        cal = Calendar(top, selectmode='day', date_pattern='dd-mm-yyyy')
        cal.pack(pady=20)
        select_button = ctk.CTkButton(top, text='Select', command=select_date)
        select_button.pack()
        
    def apply_filter(self):
        buttons = ["Salary", "House","Services", "Food", "Entertainment", "Other"]
        self.current_switch_var_on = []
        for i in range (6):
            if self.switch_var_list[i].get() == "on":
                self.current_switch_var_on.append(buttons[i])
        #print("Button status: ", self.current_switch_var_on)
        #print("start date: ", self.calendar_start_date.get(), "\n end date: ", self.calendar_end_date.get())
        print("Filters applied")
        self.refresh_data()

    def upload_file(self):
        print("Uploading file!")
        self.path = ctk.filedialog.askopenfilename(title=translations[self.language]["upload_title"], filetypes=[("CSV files", "*.csv")])
        print(self.path)
        self.refresh_data()

    def export_file(self):
        #print("Export file!")
        destination_path = ctk.filedialog.asksaveasfilename(title=translations[self.language]["export_title"], defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if destination_path:
            shutil.copy(self.path, destination_path)
            print("File exported!")
        
    def refresh_data(self):
        self.input_dialog_window = None
        column_titles = translations[self.language]["column_titles"]
        if not os.path.exists(self.path):
            self.history_non_label = ctk.CTkLabel(master=self, text=translations[self.language]["no_history"])
            self.history_non_label.grid(row=1, column=1, columnspan=3, rowspan=3, padx=20, pady=20, sticky="nsew")
        else:
            #Setting all the visual
            self.history_scrollable_frame = ctk.CTkScrollableFrame(master=self, label_text=translations[self.language]["history"])
            self.history_scrollable_frame.grid(row=1, column=1, columnspan=2, rowspan=3, sticky="nsew")
            self.filter_frame.grid(row=0, column=3, rowspan=3, sticky="nsew")
            self.filter_title.grid(row=0, column=3, padx=10, pady=10)
            self.calendar_start_date.grid(row=2, column=3, pady=10)
            self.calendar_start_date_button.grid(row=2, column=4, pady=10, padx=(0,10))
            self.calendar_end_date.grid(row=3, column=3, pady=10)
            self.calendar_end_date_button.grid(row=3, column=4, pady=10, padx=(0,10))
            self.switch_1.grid(row=4, column=3, pady=10, padx=20, sticky="nw")
            self.switch_2.grid(row=5, column=3, pady=10, padx=20, sticky="nw")
            self.switch_3.grid(row=6, column=3, pady=10, padx=20, sticky="nw")
            self.switch_4.grid(row=7, column=3, pady=10, padx=20, sticky="nw")
            self.switch_5.grid(row=8, column=3, pady=10, padx=20, sticky="nw")
            self.switch_6.grid(row=9, column=3, pady=10, padx=20, sticky="nw")
            self.filter_button.grid(row=10, column=3, pady=10, padx=20, stick="nw")

            self.graphs_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
            self.graphs_right_frame.grid(row=0, column=3, sticky="nsew")

            for idx, title in enumerate(column_titles):
                title_label = ctk.CTkLabel(self.history_scrollable_frame, text=title, font=ctk.CTkFont(size=12, weight="bold"))
                title_label.grid(row=2, column=idx, padx=10, pady=5)

            self.transaction_df = pd.read_csv(self.path)
            self.transaction_df['Comment'] = self.transaction_df['Comment'].fillna('').astype(str)

            for i in range(len(self.transaction_df)):
                if datetime.strptime(self.calendar_start_date.get(), "%d-%m-%Y") <= datetime.strptime(self.transaction_df.Date[i],"%d-%m-%Y") <= datetime.strptime(self.calendar_end_date.get(), "%d-%m-%Y"):
                    if self.transaction_df.Category[i] in self.current_switch_var_on:
                        if self.language == "English" or self.language == "Inglés":
                            type_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{self.transaction_df.Type[i]}")
                        else:
                            type_label = ctk.CTkLabel(self.history_scrollable_frame, text="Ingreso" if f"{self.transaction_df.Type[i]}" == "Income" else "Gasto")
                        type_label.grid(row=i+3, column=0, padx=10, pady=5)
                        
                        amount_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{self.transaction_df.Amount[i]}")
                        amount_label.grid(row=i+3, column=1, padx=10, pady=5)
                        
                        date_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{self.transaction_df.Date[i]}")
                        date_label.grid(row=i+3, column=2, padx=10, pady=5)
                        
                        if self.language == "English" or self.language == "Inglés":
                            category_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{self.transaction_df.Category[i]}")
                        else:
                            match self.transaction_df.Category[i]:
                                case "Salary":
                                    category_label = ctk.CTkLabel(self.history_scrollable_frame, text="Sueldo")
                                case "Other":
                                    category_label = ctk.CTkLabel(self.history_scrollable_frame, text="Otros")
                                case "House":
                                    category_label = ctk.CTkLabel(self.history_scrollable_frame, text="Casa")
                                case "Services":
                                    category_label = ctk.CTkLabel(self.history_scrollable_frame, text="Servicios")
                                case "Food":
                                    category_label = ctk.CTkLabel(self.history_scrollable_frame, text="Comida")
                                case "Entertainment":
                                    category_label = ctk.CTkLabel(self.history_scrollable_frame, text="Ocio")
                        category_label.grid(row=i+3, column=3, padx=10, pady=5)

                        comment_label = ctk.CTkLabel(self.history_scrollable_frame, text=f"{self.transaction_df.Comment[i]}")
                        comment_label.grid(row=i+3, column=4, padx=10, pady=5)
                    
        self.refresh_graphs()

    def refresh_graphs(self):
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
        
        if os.path.exists(self.path):
            income_data = {}
            expense_data = {}

            with open(self.path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for entry in reader:
                    if datetime.strptime(self.calendar_start_date.get(), "%d-%m-%Y") <= datetime.strptime(entry['Date'],"%d-%m-%Y") <= datetime.strptime(self.calendar_end_date.get(), "%d-%m-%Y"):
                        if entry['Category'] in self.current_switch_var_on:
                            category = entry.get('Category', 'N/A')
                            amount = float(entry['Amount'])
                            if entry['Type'] in ["Income", "Ingreso"]:
                                if category in income_data:
                                    income_data[category] += amount
                                else:
                                    income_data[category] = amount
                            elif entry['Type'] in ["Expense", "Gasto"]:
                                if category in expense_data:
                                    expense_data[category] += amount
                                else:
                                    expense_data[category] = amount

            my_data = []
            for category, amount in income_data.items():
                my_data.append({'Category': category, 'Amount': amount, 'Type': 'Income'})
            for category, amount in expense_data.items():
                my_data.append({'Category': category, 'Amount': amount, 'Type': 'Expense'})

            self.temp_df = pd.DataFrame(my_data)

            if self.light_mode == 'Light':
                sns.set_theme(style='white')
                text_color = 'black'
                background_color = '#DEDEDE'
            else:
                sns.set_theme(style='dark')
                text_color = 'white'
                background_color = '#2E2E2E'

            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(data=self.temp_df, x='Category', y='Amount', hue='Type', palette='pastel')
            ax.set_title(translations[self.language]["graph_title"], color=text_color)
            ax.set_xlabel(translations[self.language]["graph_category"], color=text_color)
            ax.set_ylabel(translations[self.language]["graph_amount"], color=text_color)
            xticks_labels = ax.get_xticklabels()
            legend = ax.legend(title=translations[self.language]["Type"], facecolor=background_color, edgecolor=text_color, labelcolor=text_color)
            legend.get_title().set_color(text_color)
            if self.language == "Spanish" or self.language == "Español":
                for label in xticks_labels:
                    original_text = label.get_text()
                    label.set_text(translations[self.language][original_text])
                legend_labels = legend.get_texts()
                for i in range(len(legend_labels)-1):
                    if legend_labels[i] == "Salary":
                        legend_labels[i].set_text(translations[self.language]["Income"])
                    else:
                        legend_labels[i].set_text(translations[self.language]["Expense"])
            ax.set_xticklabels(xticks_labels, rotation=0, color=text_color)
            
            heights = {}
            for p in ax.patches:
                current_height = p.get_height()
                x = p.get_x() + p.get_width() / 2
                if x not in heights:
                    heights[x] = current_height
                elif current_height > heights[x]:
                    heights[x] = current_height

            for p in ax.patches:
                current_height = p.get_height()
                x = p.get_x() + p.get_width() / 2
                if current_height == heights[x]:
                    ax.text(x, current_height + 3, f'{current_height:.0f}', ha="center", color=text_color)

            ax.set_facecolor(background_color)
            fig.patch.set_facecolor(background_color)
            ax.spines['bottom'].set_color(text_color)
            ax.spines['top'].set_color(text_color)
            ax.spines['left'].set_color(text_color)
            ax.spines['right'].set_color(text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            ax.tick_params(axis='x', colors=text_color)
            ax.tick_params(axis='y', colors=text_color)

            canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

class TopLevelWindow(ctk.CTkToplevel):
    def __init__(self, app, title):
        super().__init__()
        self.geometry("400x350")
        self.app = app
        self.title(title)
        self.init_ui()
        self.lift()
        self.focus_force()
    
    def init_ui(self):

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.dialog_event_text = ctk.CTkLabel(left_frame, text=translations[self.app.language]["dialog_event"])
        self.dialog_event_text.pack(pady=(0, 10))

        self.quantity_entry = ctk.CTkEntry(left_frame)
        self.quantity_entry.pack()

        self.category_var = IntVar()

        self.category_label = ctk.CTkLabel(right_frame, text=translations[self.app.language]["dialog_event2"])
        self.category_label.pack(pady=(0, 10))

        self.categories = translations[self.app.language]["income_categories"] if self.title() == translations[self.app.language]["add_income"] else translations[self.app.language]["expense_categories"]
        self.final_categories = translations["English"]["income_categories"] if self.title() == translations[self.app.language]["add_income"] else translations["English"]["expense_categories"]
        self.checkbuttons = []
        self.selected_list = []

        for idx, category in enumerate(self.categories):
            checkbutton = ctk.CTkCheckBox(right_frame, text=category, variable=self.category_var, onvalue=idx + 1, command=self.update_checkbuttons)
            checkbutton.pack(anchor="w", pady=(0, 5))
            self.checkbuttons.append(checkbutton)
            self.selected_list.append(0)

        self.comment_label = ctk.CTkLabel(self, text=translations[self.app.language]["dialog_event3"])
        self.comment_label.pack()

        self.comment_entry = ctk.CTkEntry(self)
        self.comment_entry.pack(padx = 10, pady=5, fill="both")
        
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady =(10, 20))

    def update_checkbuttons(self):
        selected_index = self.category_var.get() - 1
        for i in range(0, len(self.checkbuttons)):
            self.checkbuttons[i].deselect()
        self.checkbuttons[selected_index].select()

    def submit(self):
        quantity = float(self.quantity_entry.get())
        category_index = self.category_var.get() - 1
        category = self.final_categories[category_index] if category_index >= 0 else "N/A"
        date = datetime.now().strftime("%d-%m-%Y")
        comment = self.comment_entry.get()

        if self.title() == translations[self.app.language]["add_income"]:
            movement_type = "Income"
        else:
            movement_type = "Expense"

        if os.path.exists(self.app.path):
            with open(self.app.path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([movement_type, quantity, date, category, comment])
        else:
            with open(self.app.path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Type", "Amount", "Date", "Category", "Comment"])
                writer.writerow([movement_type, quantity, date, category, comment])

        self.app.refresh_data()
        self.destroy()
