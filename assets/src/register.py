from tkinter import *
import assets.src.Version2Stage0 as Version2Stage0
from assets.src.uihelpers import *


class RegisterPage(Frame, UIHelpers):
    def __init__(self, master):
        super().__init__(master, bg="#f3f4f6", name='!registerpage')

        canvas = Canvas(self, width=380, height=440, 
                        bg="#f3f4f6", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.round_rect(canvas, 5, 5, 375, 435, 25, 
                        fill="white", outline="#e5e7eb", width=2)

        content = Frame(canvas, bg="white")
        canvas.create_window(190, 220, window=content)

        Label(content, text="Sign Up", 
              font=("Segoe UI", 20, "bold"), 
              bg="white").pack(pady=(10, 35))

        self.username, self.user_var = self.make_entry(content, "Username", is_login_or_register_page=True, icon_path="userIcon.png")
        self.password, self.pass_var = self.make_entry(content, "Password", is_login_or_register_page=True, is_password=True)
        
        self.rounded_button(content, "Sign Up", self.register)

        Button(content, text="Log in", 
               command=master.show_login, 
               font=("Segoe UI", 10), 
               bg="white", fg="#06b6d4", 
               bd=0, cursor="hand2").pack(pady=(5, 15))

    def register(self):
        try:
            if self.username.get() == "" or self.password.get() == "":
                pass
            elif " " in self.username.get() or " " in self.password.get():
                pass
            else:
                Version2Stage0.register_user(
                    self.username.get().replace(" ", ""), 
                    self.password.get().replace(" ", "")
                    )
                self.master.show_login()
        except:
            pass

