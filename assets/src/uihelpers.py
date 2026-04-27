from tkinter import *
import datetime
import calendar
import locale
import sys
import os


class UIHelpers:
    def get_time_now(self):
        locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia')
        current_today = datetime.date.today()
        current_year = current_today.year
        current_month_cal = current_today.strftime("%B")
        current_numeric_day = current_today.day
        current_day_cal = current_today.strftime("%A")
        total_days_in_month = calendar.monthrange(current_year, current_today.month)[1]
        total_days_in_week = 7
        return(current_day_cal, current_numeric_day, current_month_cal, current_year, total_days_in_month, total_days_in_week)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def round_rect(self, c: Canvas, x1, y1, x2, y2, r, round_tl=True, round_tr=True, round_br=True, round_bl=True, **kwargs):

        r_tl = r if round_tl else 0
        r_tr = r if round_tr else 0
        r_br = r if round_br else 0
        r_bl = r if round_bl else 0

        points = [
                x1+r_tl, y1, 
                x2-r_tr, y1, 
                x2, y1, 
                x2, y1+r_tr, 

                x2, y2-r_br, 
                x2, y2, 
                x2-r_br, y2, 

                x1+r_bl, y2, 
                x1, y2, 
                x1, y2-r_bl, 

                x1, y1+r_tl, 
                x1, y1
        ]

        return c.create_polygon(points, smooth=True, **kwargs)

    def circular_button(self, parent, text, command, 
                                        size=50, 
                                        bg="#06b6d4", 
                                        hover="#0891b2", 
                                        fg="white", 
                                        pack_opts=None):

        canvas = Canvas(parent, 
                                        width=size, 
                                        height=size, 
                                        bg=parent["bg"], 
                                        highlightthickness=0)

        if pack_opts:
                canvas.place(**pack_opts)
        else:
                canvas.pack()

        circle = canvas.create_oval(
                2, 2, size-2, size-2, 
                fill=bg, 
                outline=bg
        )

        canvas.create_text(
                size//2, 
                (size//2)-3, 
                text=text, 
                fill=fg, 
                font=("Segoe UI", 24, "bold")
        )

        def on_enter(event):
                canvas.itemconfig(circle, fill=hover, outline=hover)

        def on_leave(event):
                canvas.itemconfig(circle, fill=bg, outline=bg)

        def on_click(event):
                command()

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

        return canvas

    def rounded_button(self, parent, text, command, 
                                   width=220, height=45, 
                                   radius=18, 
                                   bg="#06b6d4", hover="#0891b2", 
                                   fg="white", is_place_notpack=False, 
                                   pack_opts=None):

        canvas = Canvas(parent, width=width, height=height, 
                                        bg="white", highlightthickness=0)

        if pack_opts is None:
                canvas.pack(pady=10)
        elif is_place_notpack:
                canvas.place(**pack_opts)
        else:
                canvas.pack(**pack_opts)

        btn = self.round_rect(canvas, 2, 2, width-2, height-2, 
                                                  radius, fill=bg, outline=bg)

        canvas.create_text(width/2, height/2, 
                                           text=text, 
                                           fill=fg, 
                                           font=("Segoe UI", 12, "bold"))

        def on_enter(event):
                canvas.itemconfig(btn, fill=hover, outline=hover)

        def on_leave(event):
                canvas.itemconfig(btn, fill=bg, outline=bg)

        def on_click(event):
                command()

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

        return canvas
    
    def make_entry(self, parent, placeholder, icon_path=None, is_login_or_register_page = False, is_password=False):

        container = Frame(parent, bg="white")
        container.pack(pady=12, padx=30, fill="x")

        var = StringVar()

        entry = Entry(
            container, 
            textvariable=var, 
            bg="white", 
            bd=0, 
            font=("Segoe UI", 12), 
            highlightthickness=1, 
            highlightbackground="#e5e7eb")
        entry.pack(fill="x", ipady=8)

        placeholder_lbl = Label(
                container, 
                width=20, 
                text=placeholder, 
                bg="white", 
                fg="#9ca3af", 
                font=("Segoe UI", 11)
        )
        placeholder_lbl.place(x=10, y=7)

        def update_placeholder(*_):
                if var.get():
                        placeholder_lbl.place_forget()
                else:
                        placeholder_lbl.place(x=10, y=7)

        var.trace_add("write", update_placeholder)

        def focus_entry(_):
                entry.focus_set()

        entry.bind("<ButtonPress-1>", focus_entry)
        placeholder_lbl.bind("<ButtonPress-1>", focus_entry)
        entry.bind("<FocusOut>", lambda e: update_placeholder())

        if icon_path and is_login_or_register_page:
                icon = PhotoImage(file=self.resource_path(icon_path))
                entry.icon_ref = icon
                Label(container, image=icon, bg="white").place(relx=1, x=-31, y=8)

        if is_password and is_login_or_register_page:
                entry.config(show="*")

                show_icon = PhotoImage(file=self.resource_path("see.png"))
                hide_icon = PhotoImage(file=self.resource_path("unsee.png"))

                entry.show_ref = show_icon
                entry.hide_ref = hide_icon

                btn = Label(container, image=hide_icon, bg="white", cursor="hand2")
                btn.place(relx=1, x=-31, y=8)

                def toggle(_=None):
                        if entry.cget("show") == "":
                                entry.config(show="*")
                                btn.config(image=hide_icon)
                        else:
                                entry.config(show="")
                                btn.config(image=show_icon)

                btn.bind("<Button-1>", toggle)

        return entry, var
    
    def rounded_container(self, parent, bg_color="white", radius=20, padding=8, 
                      width=None, height=None, 
                      round_tl=True, round_tr=True, round_br=True, round_bl=True, is_place_notpack=False,
                      **pack_options):

        wrapper = Canvas(
                parent, 
                bg=parent["bg"], 
                highlightthickness=0
        )
        
        if is_place_notpack:
                wrapper.place(**pack_options)
        else:
                wrapper.pack(**pack_options)

        if width:
                wrapper.config(width=width)
        if height:
                wrapper.config(height=height)

        inner = Frame(wrapper, bg=bg_color)

        window_id = wrapper.create_window(
                padding, 
                padding, 
                window=inner, 
                anchor="nw"
        )

        def redraw(event=None):
                w = wrapper.winfo_width()
                h = wrapper.winfo_height()

                wrapper.delete("bg")

                self.round_rect(
                    wrapper, 
                    1, 1, 
                    w-1, h-1, 
                    radius, 
                    round_tl=round_tl, 
                    round_tr=round_tr, 
                    round_br=round_br, 
                    round_bl=round_bl, 
                    fill=bg_color, 
                    outline="#e5e7eb", 
                    width=2, 
                    tags="bg"
                )

                wrapper.coords(window_id, padding, padding)
                wrapper.itemconfig(
                        window_id, 
                        width=w - padding*2, 
                        height=h - padding*2
                )

        wrapper.bind("<Configure>", redraw)

        if height:
                wrapper.pack_propagate(False)

        return wrapper, inner
    
    def drop_down_choice(self, parent, label, options, default=None):

        Label(parent, text=label, 
                    font=("Segoe UI", 9), 
                    fg="#6b7280", bg="white").pack(anchor="w", pady=(8, 2))

        var = StringVar(value=default or options[0])

        wrapper = Frame(parent, bg="white")
        wrapper.pack(fill="x", padx=30)

        display = Label(wrapper, 
                                        textvariable=var, 
                                        anchor="w", 
                                        font=("Segoe UI", 10), 
                                        bg="#f9fafb", 
                                        bd=1, 
                                        relief="solid", 
                                        padx=10, 
                                        pady=8, 
                                        cursor="hand2")
        display.pack(fill="x")

        dropdown = Frame(wrapper, bg="white", bd=1, relief="solid")

        def select(value):
                var.set(value)
                dropdown.pack_forget()

        for opt in options:
                lbl = Label(dropdown, 
                                        text=opt, 
                                        anchor="w", 
                                        bg="white", 
                                        padx=10, 
                                        pady=6, 
                                        cursor="hand2")
                lbl.pack(fill="x")
                lbl.bind("<Button-1>", lambda e, v=opt: select(v))

        def toggle(_=None):
                if dropdown.winfo_ismapped():
                        dropdown.pack_forget()
                else:
                        dropdown.pack(fill="x")

        display.bind("<Button-1>", toggle)

        return var
    
    def bind_click_outside(self, popup, target_bind, target=""):
        def handler(event):
            x_root = event.x_root
            y_root = event.y_root
            widget = target_bind.winfo_containing(x_root, y_root)
            widget = str(widget)
            if target in widget:
                #print(widget)
                pass
            else:
                #print(widget)
                popup.destroy()            
        target_bind.bind("<Button-1>", handler)
    
    def form_error(self, parent):
        lbl = Label(parent, text="", fg="#ef4444", 
                bg="white", font=("Segoe UI", 9))
        lbl.pack(anchor="w", padx=30, pady=(4, 0))
        return lbl
