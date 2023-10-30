import customtkinter
from customtkinter import filedialog as file
from numba import jit


customtkinter.set_default_color_theme("D:/code/shift/theme.json")
customtkinter.deactivate_automatic_dpi_awareness()

MONTHS = {"jan":31,"feb":28,"mar":31,"apr":30,"may":31,"jun":30,"jul":31,"aug":31,"sep":30,"oct":31,"nov":30,"dec":31}

def add_ppl(): ...

def rem_ppl(): ...

def date_config(): ...



class App(customtkinter.CTk):
    def submit(*args):...
    def __init__(self):
        super().__init__()

        customtkinter.AppearanceModeTracker.set_appearance_mode("dark")
        customtkinter.deactivate_automatic_dpi_awareness()

        self.geometry("500x500")
        self.resizable(False, False)
        self.title("Shift calculator")

        self.frame = customtkinter.CTkFrame(self, width=1000, height=1000, corner_radius=0)
        self.frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=75)
        self.frame.grid_rowconfigure(4, weight=1)

        self.add = customtkinter.CTkButton(self.frame, text="Add", command=add_ppl, width=10, height=10)
        self.add.grid(row=0, column=1, padx=5, pady=20)

        self.add_e = customtkinter.CTkEntry(self.frame, placeholder_text="Add people")
        self.add_e.grid(row=0, column=0, padx=5, pady=20)

        self.rem = customtkinter.CTkButton(self.frame, text="Remove", command=rem_ppl, width=10, height=15)
        self.rem.grid(row=2, column=1, padx=5, pady=20)

        self.rem_e = customtkinter.CTkEntry(self.frame, placeholder_text="Remove people")
        self.rem_e.grid(row=2, column=0, padx=5, pady=20)

        self.frame_2 = customtkinter.CTkFrame(self, width=1000, height=1000, corner_radius=0)
        self.frame_2.grid(row=10, column=1, sticky="nsew", padx=75)

        self.date_label = customtkinter.CTkLabel(self.frame_2, text="Month")
        self.date_label.grid(row=3, column=1, pady=10)

        self.month = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False,
            values=["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])
        self.month.grid(row=4, column=1, padx=75, pady=0)

        self.year = customtkinter.CTkEntry(self.frame_2, placeholder_text="Year")
        self.year.grid(row=5, column=1, pady=10)


        self.file_e = customtkinter.CTkEntry(self.frame_2, placeholder_text="Input file path")
        self.file_e.grid(row=6, column=1)

        self.file_b = customtkinter.CTkButton(self.frame_2, text="browse", command=self.browse)
        self.file_b.grid(row=7, column=1, pady=20)

        self.submit_b = customtkinter.CTkButton(self.frame_2, text="Submit", command=self.submit)
        self.submit_b.grid(row=10, column=1, pady=50)



    def is_leap_year(self, year):
        year = int(year)
        if not(year % 4 == 0):
            return False
        elif not(year % 100 == 0):
            return True
        elif not(year % 400 == 0):
            return False
        else:
            return True


    def browse(*args):
        global path
        path = file.askopenfile(filetypes=(("csv files", "*.csv"),
                                ("excel files", "*.xlsx"),
                                ("excel files", "*.xlsm"),
                                ("excel files", "*.xlsb"),
                                ("excel files", "*.xltx"),
                                ("all files", "*.*")),
                                title="Choose a file",)

def main():
    if __name__ == "__main__":
        app = App()
        app.iconbitmap("calendar.ico")
        app.mainloop()
main()
