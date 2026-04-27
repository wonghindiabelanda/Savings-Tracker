from tkinter import *
import assets.src.Version2Stage0 as Version2Stage0
from assets.src.uihelpers import *


class LoginPage(Frame, UIHelpers):
    def __init__(self, master):
        super().__init__(master, bg="#f3f4f6", name='!loginpage')

        canvas = Canvas(self, width=380, height=440, 
                        bg="#f3f4f6", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.round_rect(canvas, 5, 5, 375, 435, 25, 
                        fill="white", outline="#e5e7eb", width=2)

        content = Frame(canvas, bg="white")
        canvas.create_window(190, 220, window=content)

        Label(content, text="Log in", 
              font=("Segoe UI", 20, "bold"), 
              bg="white").pack(pady=(10, 35))

        self.username, self.user_var = self.make_entry(content, "Username", is_login_or_register_page=True, icon_path="userIcon.png")
        self.password, self.pass_var = self.make_entry(content, "Password", is_login_or_register_page=True, is_password=True)
        
        self.rounded_button(content, "Log in", self.login)

        Button(content, text="Sign Up", 
               command=master.show_register, 
               font=("Segoe UI", 10), 
               bg="white", fg="#06b6d4", 
               bd=0, cursor="hand2").pack(pady=(5, 15))

    def login(self):
        user_id = Version2Stage0.login_user(
            self.username.get(), 
            self.password.get()
        )
        if user_id:
            self.master.show_dashboard(user_id)

