from .front import App, MONTHS

class AppScript(App):
    def __init__(self):
        super().__init__()
    
    def check_app(self):
        if self.month.get() in MONTHS.keys():
            print(self.month.get())
    
    def submit():
        print("hi")