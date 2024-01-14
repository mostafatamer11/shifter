import customtkinter as ctk
from .widgets import *
from tkinter.messagebox import Message as CTkMessage
from tkinter.messagebox import ERROR
from ..core import generate, file_gen


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.version = 0.1
        self.title(f"Shifts v{self.version}")
        self.geometry("650x400")
        self.minsize(600, 400)
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self.main = Main(self)

        self.bar = TopBar(self, self.main)

        self.generate = GenerateFrame(self)

    def run(self):
        self.mainloop()


class TopBar(ctk.CTkFrame):
    def __init__(self, master, main):
        super().__init__(master, fg_color="transparent")
        self.main = main
        self.display()
        self.widgets()

    def display(self):
        self.place(x=0, y=0, relwidth=1, relheight=0.05)

    def widgets(self):
        self.rowconfigure((0), weight=1, uniform="a")
        self.columnconfigure((1, 2, 3, 4), weight=1, uniform="a")
        self.columnconfigure((0), weight=2, uniform="a")

        def dark_mode_switch():
            if self.app_mode.get() == 1:
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        self.app_mode = ctk.CTkSwitch(self, text="Dark Mode",
            command=dark_mode_switch)
        self.app_mode.select()
        self.app_mode.grid(row=0, column=4, sticky="w")

        def resizable_lock():
            if self.resizable_switch.get() == 1:
                self.master.resizable(True, True)
            else:
                self.master.resizable(False, False)
        self.resizable_switch = ctk.CTkSwitch(self, text="Resizable",
            command=resizable_lock)
        self.resizable_switch.grid(row=0, column=3)

        def selection_callback(*args):
            self.main.selected = self.selection_var.get()
        self.selection_var = ctk.StringVar(value="employees(no one selected)")
        self.selection = ctk.CTkOptionMenu(self, variable=self.selection_var, command=selection_callback, state="disabled")
        self.selection.grid(row=0, column=0, columnspan=1, sticky="w")

        months = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]
        self.month_str = ""
        def month_callback(*arg):
            self.month_str = self.month.get()
        self.month = ctk.StringVar(value="select month(not required)")
        self.menu_master = ctk.CTkOptionMenu(self, variable=self.month, command=month_callback)
        self.menu_master.configure(values=months)
        self.menu_master.grid(row=0, column=1, columnspan=2, sticky="w")

    def add_employee(self):
        self.selection_var.set(value="employees")
        self.selection.configure(values=list(self.main.vications.keys()), state="normal")

    def update(self):
        if len(self.main.vications.keys()) == 0:
            self.selection_var.set(value="employees(no one selected)")
            self.selection.configure(values=[], state="disabled")

        else:
            self.selection_var.set(value="employees")
            self.selection.configure(values=list(self.main.vications.keys()), state="normal")

    def remove_employee(self):
        self.update()


class Main(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.vications = dict()
        self.selected = ctk.StringVar()
        self.employees = set()
        self.display()
        self.widgets()

    def display(self):
        self.place(x=0, rely=0.05, relwidth=0.7, relheight=0.95)

    def widgets(self):
        self.control_frame = ControlFrame(self)

    def add_employee_frame(self):
        self.add_frame = AddFrame(self)

    def add_employee(self, name, vications):
        self.vications[name] = vications
        self.employees.add(name)
        self.master.bar.add_employee()

    def remove_employee(self):
        if not isinstance(self.selected, ctk.StringVar):
            print(self.selected)
            self.vications.pop(self.selected)
            self.employees.remove(self.selected)
            self.master.bar.remove_employee()


class AddFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.frames:list[VicationFrame] = []
        self.employee = None
        self.display()
        self.widgets()
        self._master = master

    def display(self):
        self.pack(side="left", fill="both", ipadx=1000)

    def widgets(self):
        self.name_label = ctk.CTkLabel(self, text="Name: ")
        self.name_label.pack(pady=10, side="top")

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your name")
        self.name_entry.pack(ipadx=1000, pady=10, side="top")
        self.name_entry.focus_force()

        def vication_callback():
            self.vication_button.pack_forget()
            self.add_employee.pack_forget()

            frame = VicationFrame(self)
            self.frames.append(frame)

            self.vication_button.pack(side="top", pady=30)
            self.add_employee.pack(side="top", pady=20)
        self.vication_button = ctk.CTkButton(self, text="Add vication", command=vication_callback)
        self.vication_button.pack(side="top", pady=30)

        def add_callback():
            flag = False
            vications = [] if self.frames else None
            if self.name_entry.get() == "":
                error_label = CTkMessage(self, title="Error", icon=ERROR,
                                        message="Name not given")
                flag = True
                error_label.show()

            if isinstance(vications, list):
                for indx, frame in enumerate(self.frames):
                    temp = (frame.from_entry.get(), frame.to_entry.get())
                    if temp == (0, 0):
                        frame.destroy()
                        continue

                    elif temp[0] > temp[1] :
                        error_label = CTkMessage(self, title="Error", icon=ERROR,
                                                message=f"\"From: {temp[0]}\" is greater than \"To: {temp[1]}\"\n\
in vication {indx + 1}")
                        error_label.show()
                        flag = True

                    if not flag:
                        vications.append(temp)

                    else:
                        vications = []
            if not flag:
                self._master.add_employee(self.name_entry.get(), vications)
                self.pack_forget()
                self.destroy()
        self.add_employee = ctk.CTkButton(self, text="Add", command=add_callback)
        self.add_employee.pack(side="top", pady=20)


class VicationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.display()
        self.widgets()

    def display(self):
        self.pack(pady=10, ipadx=100)

    def widgets(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure((1, 2), weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure((0, 1), weight=3)

        self.remove_button = ctk.CTkButton(self, text="x", width=10, height=10, command=self.remove)
        self.remove_button.grid(row=0, column=2)

        self.from_label = ctk.CTkLabel(self, text="From:")
        self.from_label.grid(row=1, column=0, sticky="w")

        self.from_entry = IntSpinbox(self)
        self.from_entry.grid(row=1, column=1, sticky="we", columnspan=2, pady=10)

        self.to_label = ctk.CTkLabel(self, text="To:")
        self.to_label.grid(row=2, column=0, sticky="w")

        self.to_entry = IntSpinbox(self)
        self.to_entry.grid(row=2, column=1, sticky="we", columnspan=2, pady=10)

    def remove(self):
        self.destroy()
        self.master.frames.remove(self)


class ControlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.dispaly()
        self.widgets()

    def dispaly(self):
        self.pack(side="left", fill="both", ipadx=20, padx=10)

    def widgets(self):
        self.add_button = ctk.CTkButton(self, text="Add Employee", command=self.master.add_employee_frame)
        self.add_button.pack(pady=10)

        self.remove_button = ctk.CTkButton(self, text="Remove Employee", command=self.master.remove_employee)
        self.remove_button.pack(pady=30)


class GenerateFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.file_path = ctk.StringVar()
        self.display()
        self.widgets()

    def display(self):
        self.place(relx=0.7, rely=0.05, relwidth=0.3, relheight=0.95)

    def widgets(self):
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.place(rely=0.1, relheight=0.3, relwidth=1)

        self.label = ctk.CTkLabel(self.frame, text="Enter file path:")
        self.label.pack()

        self.entry = ctk.CTkEntry(self.frame, textvariable=self.file_path)
        self.entry.pack(padx=5, ipadx=1000)

        def new_callback():
            self.file_path.set(ctk.filedialog.asksaveasfilename())
        self.new = ctk.CTkButton(self, text="New file", command=new_callback)
        self.new.place(rely=0.5, relx=0.2, relwidth=0.5)

        def open_callback():
            self.file_path.set(ctk.filedialog.askopenfilename())
        self.new = ctk.CTkButton(self, text="Open file", command=open_callback)
        self.new.place(rely=0.6, relx=0.2, relwidth=0.5)

        def generate_callback():
            month = self.master.bar.month_str if not len(self.master.bar.month_str) == 0 else None
            if len(self.master.main.vications) == 0:
                error_label = CTkMessage(self, title="Error", icon=ERROR,
                                            message="Employees not given")
                error_label.show()
            elif len(self.file_path.get()) == 0:
                error_label = CTkMessage(self, title="Error", icon=ERROR,
                            message="File not given")
                error_label.show()
            else:
                file_gen(generate(self.master.main.vications, month), self.file_path.get())
                congrats = CTkMessage(self, title="Congrats", message="Done succesfully!")
                congrats.show()
        self.generate = ctk.CTkButton(self, text="Generate file", command=generate_callback)
        self.generate.place(rely=0.7, relx=0.2, relwidth=0.5)

