from tkinter import *
from assets.src.uihelpers import *


class AboutPage(Frame, UIHelpers):
    def __init__(self, master):
        super().__init__(master, bg="#f3f4f6", name='!aboutpage')
        self.master = master
        self.user_id = master.current_user_id

        def show_dashboard():
            master.show_dashboard(self.user_id)
                 
        top_wrapper, top = self.rounded_container(self, bg_color="white", radius=18, padding=0, height=50, padx=0, pady=(0, 5), fill="x", round_tl=False, round_tr=False, round_br=True, round_bl=True)

        time_data = self.get_time_now()
        self.time_data = time_data
        Label(
            top, 
            text=f"{time_data[0]}, {time_data[1]} {time_data[2]}, {time_data[3]}", 
            font=("Segoe UI", 11), 
            bg="white", 
            fg="#6b7280"
        ).place(relx=0.5, rely=0.5, anchor="center")

        more_settings_icon = PhotoImage(file=self.resource_path("hamburgermenu.png"))
        self.more_settings_icon = more_settings_icon

        more_btn = Label(top, image=more_settings_icon, bg="white", cursor="hand2")
        more_btn.place(relx=1.0, x=-12, rely=0.5, anchor="e")

        def more_settings(event=None):
                wrapper_hamburg, hamburg_more_settings = self.rounded_container(self, bg_color="white", is_place_notpack=True, radius=18, padding=6, height=120, width=240, anchor="center", relx=0.87, rely=0.1)
                btn_row = Frame(hamburg_more_settings, bg="white")
                btn_row.pack(pady=10, fill="x")

                dashboard_btn = Label(wrapper_hamburg, text="Beranda", font=("Helvetica", 12, "bold"), bg="white", fg="#838383")
                wrapper_hamburg.create_window(120, 43, window=dashboard_btn)
                def trigger_dashboard(_=None):
                    show_dashboard()
                dashboard_btn.bind("<Button-1>", trigger_dashboard)
                dashboard_btn.bind("<Enter>", lambda e: dashboard_btn.config(fg="#9ca3af"))
                dashboard_btn.bind("<Leave>", lambda e: dashboard_btn.config(fg="#838383"))

                self.rounded_button(wrapper_hamburg, "Logout", self.logout, 120, 35, 12, "#ef4444", "#dc2626", "white", is_place_notpack=True, pack_opts={"anchor": "center", "relx": 0.5, "rely": 0.7})
                
                self.bind_click_outside(popup=wrapper_hamburg, target_bind=self.master, target=".!aboutpage.!canvas")

        more_btn.bind("<Button-1>", more_settings)

        g_r = (1 + 5**0.5) / 2
        width_about_sec = self.winfo_screenwidth() - 12
        height_about_sec = 500
        width_about_sec_left = int(width_about_sec / (g_r * 3))
        width_about_sec_right = width_about_sec - width_about_sec_left
        sec_row = Frame(self, bg="#f3f4f6")
        sec_row.pack(pady=10, fill="x")
        wrapper_about_sec_left, about_sec_left = self.rounded_container(sec_row, bg_color="white", is_place_notpack=False, radius=50, padding=50, height=height_about_sec, width=width_about_sec_left, round_br=False, round_tr=False, fill="x", side="left", padx=4, pady=10)
        wrapper_about_sec_right, about_sec_right = self.rounded_container(sec_row, bg_color="white", is_place_notpack=False, radius=50, padding=50, height=height_about_sec, width=width_about_sec_right, round_bl=False, round_tl=False, fill="x", side="right", padx=4, pady=10)

        self.about_sec_right = about_sec_right
        
        self.content_frame = Frame(about_sec_right, bg="white")
        self.content_frame.pack(fill="both", expand=True)
        self.show_content("creator")

        self.rounded_button(
            about_sec_left,
            "Pembuat",
            lambda: self.show_content("creator"),
            width=width_about_sec_left-100
            )
        self.rounded_button(
            about_sec_left,
            "Tentang Aplikasi Ini",
            lambda: self.show_content("about"),
            width=width_about_sec_left-100
            )
        self.rounded_button(
            about_sec_left,
            "Lihat Portofolio",
            lambda: self.show_content("portfolio"),
            width=width_about_sec_left-100
            )
        
    def show_content(self, section):

        for widget in self.content_frame.winfo_children():
                widget.destroy()

        container = Frame(self.content_frame, bg="white")
        container.pack(fill="both", expand=True)

        if section == "creator":

                Label(
                        container,
                        text="Pembuat",
                        font=("Segoe UI", 26, "bold"),
                        bg="white",
                        fg="#111827"
                ).pack(anchor="w", pady=(0,10))

                Frame(container, bg="#e5e7eb", height=2).pack(fill="x", pady=(0,20))

                Label(
                        container,
                        text="Pembuat aplikasi ini:",
                        font=("Segoe UI", 12),
                        bg="white",
                        fg="#6b7280"
                ).pack(anchor="w", pady=(0,20))

                creators = [
                        "Muhammad Reytama Putra Permana — Full Stack Developer",
                ]

                for c in creators:
                        Label(
                                container,
                                text="• " + c,
                                font=("Segoe UI", 12),
                                bg="white",
                                fg="#374151"
                        ).pack(anchor="w", pady=4)


        elif section == "about":

                Label(
                        container,
                        text="Tentang aplikasi ini",
                        font=("Segoe UI", 26, "bold"),
                        bg="white",
                        fg="#111827"
                ).pack(anchor="w", pady=(0,10))

                Frame(container, bg="#e5e7eb", height=2).pack(fill="x", pady=(0,20))

                Label(
                        container,
                        text="""
Saya membuat aplikasi ini dengan bertujuan untuk memfasilitasi ketika kita perlu mencatat tabungan.
Dan karena tugas sekolah :v. 

Saya berharap aplikasi ini memenuhi tujuannya. 

Maafkan saya jika aplikasi ini tidak memenuhi tujuannya.
Dan maafkan saya karena penjelasan tentang aplikasi ini itu sangat pendek :v. 
""",
                        font=("Segoe UI", 12),
                        bg="white",
                        fg="#374151",
                        justify="left",
                        wraplength=650
                ).pack(anchor="w")


        elif section == "portfolio":

                Label(
                        container,
                        text="Portfolio",
                        font=("Segoe UI", 26, "bold"),
                        bg="white",
                        fg="#111827"
                ).pack(anchor="w", pady=(0,10))

                Frame(container, bg="#e5e7eb", height=2).pack(fill="x", pady=(0,20))

                Label(
                        container,
                        text="Hal-hal yang dibuat oleh M. Reytama P. P.",
                        font=("Segoe UI", 12),
                        bg="white",
                        fg="#6b7280"
                ).pack(anchor="w", pady=(0,20))

                projects = [
                        "Savings Tracker App",
                        "Minimax TicTacToe Algorithm"
                ]

                for project in projects:
                        Label(
                                container,
                                text="• " + project,
                                font=("Segoe UI", 12),
                                bg="white",
                                fg="#374151"
                        ).pack(anchor="w", pady=4)

    def logout(self):
        self.master.show_login()
