from tkinter import *
import assets.src.Version2Stage0 as Version2Stage0
from assets.src.uihelpers import *
from assets.src.savingsrenderer import *


class DashboardPage(Frame, UIHelpers):
    def __init__(self, master):
        super().__init__(master, bg="#f3f4f6", name='!dashboardpage')
        self.master = master

        def show_about():
            self.master.show_about()

        top_wrapper, top = self.rounded_container(self, bg_color="white", radius=18, padding=0, height=50, padx=0, pady=(0, 5), fill="x", round_tl=False, round_tr=False, round_br=True, round_bl=True)

        txt_widget = Text(top, font=("Segoe UI", 16, "bold"), bg="white", height=1, borderwidth=0, highlightthickness=0)
        txt_widget.pack(side="left", padx=12)

        username = Version2Stage0.get_user_by_id(self.master.current_user_id)['username']
        txt_widget.insert(END, "Halo, ")
        txt_widget.insert(END, f"{username}!")

        txt_widget.tag_add("color_user", "1.3", "end") 
        txt_widget.tag_config("color_user", foreground="#06b6d4")

        txt_widget.config(state="disabled")

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

                misc_btn = Label(wrapper_hamburg, text="Hal Yang Lainnya", font=("Helvetica", 12, "bold"), bg="white", fg="#838383")
                misc_btn.place()
                wrapper_hamburg.create_window(120, 43, window=misc_btn)
                def trigger_misc(_=None):
                    show_about()
                misc_btn.bind("<Button-1>", trigger_misc)
                misc_btn.bind("<Enter>", lambda e: misc_btn.config(fg="#9ca3af"))
                misc_btn.bind("<Leave>", lambda e: misc_btn.config(fg="#838383"))

                self.rounded_button(wrapper_hamburg, "Logout", self.logout, 120, 35, 12, "#ef4444", "#dc2626", "white", is_place_notpack=True, pack_opts={"anchor": "center", "relx": 0.5, "rely": 0.7})
                
                self.bind_click_outside(popup=wrapper_hamburg, target_bind=self.master, target=".!dashboardpage.!canvas")

        more_btn.bind("<Button-1>", more_settings)

        container = Frame(self, bg="#f3f4f6")
        container.pack(fill="both", expand=True)


        summary_container = Frame(container, bg="#f3f4f6")
        summary_container.pack(fill="x", padx=4, pady=5)

        self.total_goal_lbl = self.create_summary_card(summary_container, "Total Tabungan")
        self.total_target_lbl = self.create_summary_card(summary_container, "Total Target Menabung")
        self.total_saved_lbl = self.create_summary_card(summary_container, "Total Tertabung")

        self.canvas = Canvas(container, bg="#f3f4f6", highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.goal_container = Frame(self.canvas, bg="#f3f4f6")

        self.goal_container.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.goal_container, 
            anchor="nw"
        )

        def resize_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", resize_canvas)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all(
             "<MouseWheel>", 
             lambda ev: self.canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.circular_button(self.canvas, "+", self.add_goal_popup, size=55, pack_opts={"relx": 1.0, "rely": 1.0, "anchor": "se", "x": -15, "y": -15})
        self.load_goals()

    def create_summary_card(self, parent, title):
        ui = UIHelpers()

        wrapper, card = self.rounded_container(parent, bg_color="white", radius=18, padding=6, height=150, width=280, side="left", padx=10)
        
        Label(
            card, 
            text=title, 
            font=("Segoe UI", 11), 
            fg="#6b7280", 
            bg="white"
        ).pack(anchor="w")

        value = Label(
            card, 
            text="0", 
            font=("Segoe UI", 15, "bold"), 
            bg="white"
        )
        value.pack(anchor="w", pady=(4, 0))

        return value

    
    def load_goals(self):
        for widget in self.goal_container.winfo_children():
            widget.destroy()

        goals = Version2Stage0.get_goals(self.master.current_user_id)

        total_target = 0
        total_saved = 0

        for goal in goals:
            SavingsCard(self.goal_container, goal, self).pack(
                pady=15, padx=4, fill="x"
            )

            goal_id, name, target, nominal = goal
            total_target += target

            boxes = Version2Stage0.get_boxes(goal_id)
            checked = sum(boxes.values())
            total_saved += checked * nominal

        self.total_goal_lbl.config(text=str(len(goals)))
        self.total_target_lbl.config(text=f"Rp {total_target:,}")
        self.total_saved_lbl.config(text=f"Rp {total_saved:,}")

    PERIOD_MAP = {
    "7 Hari": 7,
    "1 Bulan": lambda d: d,
    "2 Bulan": lambda d: d * 2,
    "3 Bulan": lambda d: d * 3,
    }

    FREQ_MAP = {
    "SetiapHari": lambda d: d,
    "SetiapMinggu": lambda d: d // 7,
    "SetiapBulan": lambda d: max(1, d // 30),
    }

    def resolve_period(self, label):
        val = self.PERIOD_MAP[label]
        return val(self.time_data[4]) if callable(val) else val

    def resolve_frequency(self, label, days):
        return self.FREQ_MAP[label](days)
    
    def add_goal_popup(self):

        canvas = Canvas(self, width=420, height=560, 
                                                                        bg="#f3f4f6", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.round_rect(canvas, 5, 5, 415, 555, 25, 
                                                                        fill="white", outline="#e5e7eb", width=2)

        content = Frame(canvas, bg="white")
        canvas.create_window(210, 280, window=content, width=360)
        
        close_btn = Label(canvas, text="✕", font=("Helvetica", 20, "bold"), bg="white", fg="#9ca3af", cursor="hand2")
        canvas.create_window(390, 44, window=close_btn)

        def close_popup(_=None):
                canvas.destroy()

        close_btn.bind("<Button-1>", close_popup)
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg="#ef4444"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg="#9ca3af"))

        Label(content, text="Buat Target Menabung Baru", 
                                font=("Segoe UI", 13, "bold"), 
                                bg="white").pack(pady=(10, 15))
        
        def field(label):
                Label(content, text=label, 
                                        font=("Segoe UI", 9), 
                                        fg="#6b7280", 
                                        bg="white").pack(anchor="w", pady=(8, 2))
                entry, _ = self.make_entry(content, "")
                return entry

        goal_name = field("Tujuan Menabung")
        nominal = field("Nominal Per Save")

        period = self.drop_down_choice(content, "Jangka Menabung", 
                                                                     list(self.PERIOD_MAP.keys()), "1 Bulan")

        habit = self.drop_down_choice(content, "Menabung Per", 
                                                                    list(self.FREQ_MAP.keys()), "Everyday")

        error_lbl = self.form_error(content)

        preview_lbl = Label(content, 
                                                text="", 
                                                fg="#6b7280", 
                                                bg="white", 
                                                font=("Segoe UI", 9))
        preview_lbl.pack(pady=10)

        def update_preview(*_):
                try:
                        n = int(nominal.get())

                        days = self.resolve_period(period.get())
                        total = self.resolve_frequency(habit.get(), days)

                        preview_lbl.config(
                                text=f"Total Tertabung: Rp {n*total:,} dalam waktu {days} hari ({total}x menabung)"
                        )
                except:
                        preview_lbl.config(text="")

        nominal.bind("<KeyRelease>", update_preview)
        period.trace_add("write", update_preview)
        habit.trace_add("write", update_preview)

        def save():

                if not goal_name.get():
                        error_lbl.config(text="Tujuan Menabung wajib di isi")
                        return

                try:
                        n = int(nominal.get())
                except:
                        error_lbl.config(text="Nominal harus berupa angka")
                        return

                days = self.resolve_period(period.get())
                total = self.resolve_frequency(habit.get(), days)
                target = total * n

                Version2Stage0.create_goal(
                        self.master.current_user_id, 
                        goal_name.get(), 
                        target, 
                        n
                )

                canvas.destroy()
                self.load_goals()

        self.rounded_button(content, "Buat Target Menabung Baru", save, 355, 50, 10, "#06b6d4", "#0891b2", "white")

        self.bind_click_outside(popup=canvas, target_bind=self.master, target=".!dashboardpage.!canvas")

    def add_goal_popup_edit(self, goal_card):

        canvas = Canvas(self, width=420, height=560, 
                                                                        bg="#f3f4f6", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.round_rect(canvas, 5, 5, 415, 555, 25, 
                                                                        fill="white", outline="#e5e7eb", width=2)

        content = Frame(canvas, bg="white")
        canvas.create_window(210, 280, window=content, width=360)

        close_btn = Label(canvas, text="✕", font=("Helvetica", 20, "bold"), bg="white", fg="#9ca3af", cursor="hand2")
        canvas.create_window(390, 44, window=close_btn)

        def close_popup(_=None):
                canvas.destroy()

        close_btn.bind("<Button-1>", close_popup)
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg="#ef4444"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg="#9ca3af"))

        Label(content, text="Edit Target Menabung", 
                                font=("Segoe UI", 13, "bold"), 
                                bg="white").pack(pady=(10, 15))

        def field(label, default=""):
                Label(content, text=label, 
                                        font=("Segoe UI", 9), 
                                        fg="#6b7280", 
                                        bg="white").pack(anchor="w", pady=(8, 2))
                entry, _ = self.make_entry(content, default)
                return entry

        goal_name = field("Tujuan Menabung", goal_card.name)
        nominal = field("Nominal Per Save", str(goal_card.nominal))

        period = self.drop_down_choice(content, "Jangka Menabung", 
                                                                     list(self.PERIOD_MAP.keys()), "1 Bulan")

        habit = self.drop_down_choice(content, "Menabung Per", 
                                                                    list(self.FREQ_MAP.keys()), "Everyday")

        error_lbl = self.form_error(content)

        preview_lbl = Label(content, 
                                                text="", 
                                                fg="#6b7280", 
                                                bg="white", 
                                                font=("Segoe UI", 9))
        preview_lbl.pack(pady=10)

        # ===== PREVIEW =====
        def update_preview(*_):
                try:
                        n = int(nominal.get())

                        days = self.resolve_period(period.get())
                        total = self.resolve_frequency(habit.get(), days)

                        preview_lbl.config(
                                text=f"Total Tertabung: Rp {n*total:,} dalam waktu {days} hari ({total}x menabung)"
                        )
                except:
                        preview_lbl.config(text="")

        nominal.bind("<KeyRelease>", update_preview)
        period.trace_add("write", update_preview)
        habit.trace_add("write", update_preview)

        update_preview()

        # ===== SAVE =====
        def save():
                error_lbl.config(text="")

                if not goal_name.get():
                        error_lbl.config(text="Tujuan Menabung wajib di isi")
                        return

                try:
                        n = int(nominal.get())
                except:
                        error_lbl.config(text="Nominal harus berupa angka")
                        return

                days = self.resolve_period(period.get())
                total = self.resolve_frequency(habit.get(), days)
                target = total * n

                Version2Stage0.update_goal(
                        goal_card.goal_id, 
                        goal_name.get(), 
                        target, 
                        n
                )

                canvas.destroy()
                self.load_goals()

        self.rounded_button(content, "Update Target Menabung", save, 355, 50, 10, "#06b6d4", "#0891b2", "white")

        self.bind_click_outside(popup=canvas, target_bind=self.master, target=".!dashboardpage.!canvas")

    def open_delete_goal_popup(self, goal_card):

        canvas = Canvas(self, width=380, height=220, 
                                        bg="#f3f4f6", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.round_rect(canvas, 5, 5, 375, 215, 25, 
                                        fill="white", outline="#e5e7eb", width=2)

        content = Frame(canvas, bg="white")
        canvas.create_window(190, 110, window=content, width=300)

        Label(content, 
                    text="Hapus Target Menabung", 
                    font=("Segoe UI", 13, "bold"), 
                    bg="white").pack(pady=(10, 5))

        Label(content, 
                    text=f"Apakah kamu benar ingin menghapus ini?\n“{goal_card.name}” ?", 
                    font=("Segoe UI", 10), 
                    fg="#6b7280", 
                    bg="white", 
                    justify="center").pack(pady=10)

        btn_row = Frame(content, bg="white")
        btn_row.pack(pady=10, fill="x")

        def cancel():
                canvas.destroy()

        def confirm():
                Version2Stage0.delete_goal(goal_card.goal_id)
                canvas.destroy()
                self.load_goals()

        self.rounded_button(btn_row, "Batalkan", cancel, 120, 35, 6, "white", "#e5e7eb", "black", pack_opts={"side": "left", "padx": 8})
        self.rounded_button(btn_row, "Hapus Target Menabung Ini", confirm, 120, 35, 6, "#ef4444", "#dc2626", "white", pack_opts={"side": "left", "padx": 8})


        self.bind_click_outside(popup=canvas, target_bind=self.master, target=".!dashboardpage.!canvas")

    def logout(self):
        self.master.show_login()

    def update_total_saved(self, delta):
        current_text = self.total_saved_lbl.cget("text")
        current_value = int(current_text.replace("Rp", "").replace(",", "").replace(".", "").strip())
        new_value = current_value + delta
        self.total_saved_lbl.config(text=f"Rp {new_value:,}")
