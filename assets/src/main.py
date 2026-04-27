from tkinter import *
import assets.src.Version2Stage0 as Version2Stage0
from assets.src.login import *
from assets.src.register import *
from assets.src.dashboard import *
from assets.src.about import *
from assets.src.uihelpers import *

class App(Tk, UIHelpers):
    def __init__(self):
        super().__init__()

        self.title("Savings Tracker")
        self.geometry("1000x650")
        self.configure(bg="#f3f4f6")
        icon = PhotoImage(file=self.resource_path("favicon.png"))
        self.iconphoto(True, icon)

        Version2Stage0.setup()

        self.current_user_id = None
        self.current_frame = None

        self.show_login()

    def switch_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.switch_frame(LoginPage)

    def show_register(self):
        self.switch_frame(RegisterPage)

    def show_dashboard(self, user_id):
        self.current_user_id = user_id
        self.switch_frame(DashboardPage)
    
    def show_about(self):
        self.switch_frame(AboutPage)


if __name__ == "__main__":
    app = App()
    app.mainloop()