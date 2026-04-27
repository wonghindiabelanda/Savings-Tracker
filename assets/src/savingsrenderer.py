from tkinter import *
import assets.src.Version2Stage0 as Version2Stage0
from assets.src.uihelpers import *


BOX_AREA_HEIGHT = 140

BOX_SIZE = 28

class SavingsCard(Frame, UIHelpers):

    COLS = 15

    def __init__(self, master, goal, dashboard):
        Frame.__init__(self, master, bg=master["bg"])
        ui = UIHelpers()

        wrapper, card = self.rounded_container(self, bg_color="white", radius=18, padding=10, height=300, width=600, side="left", padx=10, pady=10)

        self.card = card
        self.dashboard = dashboard
        self.app = dashboard.master

        self.goal_id, self.name, self.target, self.nominal = goal
        self.total_boxes = self.target // self.nominal

        header = Frame(self.card, bg="white")
        header.pack(fill="x")

        Label(header, text=self.name, font=("Segoe UI", 14, "bold"), bg="white").pack(side="left")

        more_settings_icon = PhotoImage(file=self.resource_path("3dots.png"))
        self.more_settings_icon = more_settings_icon

        more_btn = Label(header, image=more_settings_icon, bg="white", cursor="hand2")
        more_btn.pack(side="right", padx=5)
        def more_settings(event=None):
                wrapper_more_btn, more_settings_btn = self.rounded_container(self, bg_color="#FCFCFC", is_place_notpack=True, radius=18, padding=6, height=60, width=79, anchor="center", x=more_btn.winfo_x()+40, rely=0.1)
                self.wrapper_more_btn = wrapper_more_btn
                delete_btn = Label(wrapper_more_btn, text="Delete", font=("Helvetica", 12, "bold"), bg="#FCFCFC", fg="#838383")
                wrapper_more_btn.create_window(31.5, 43, window=delete_btn)
                def trigger_delete(_=None):
                    self.delete_goal()
                delete_btn.bind("<Button-1>", trigger_delete)
                delete_btn.bind("<Enter>", lambda e: delete_btn.config(fg="#9ca3af"))
                delete_btn.bind("<Leave>", lambda e: delete_btn.config(fg="#838383"))

                edit_btn = Label(wrapper_more_btn, text="Edit", font=("Helvetica", 12, "bold"), bg="#FCFCFC", fg="#838383")
                wrapper_more_btn.create_window(22.5, 18, window=edit_btn)
                def trigger_edit(_=None):
                    self.edit_goal()
                edit_btn.bind("<Button-1>", trigger_edit)
                edit_btn.bind("<Enter>", lambda e: edit_btn.config(fg="#9ca3af"))
                edit_btn.bind("<Leave>", lambda e: edit_btn.config(fg="#838383"))

                self.bind_click_outside(popup=wrapper_more_btn, target_bind=self.app, target="!dashboardpage.!frame.!canvas.!frame.!SavingsCard.!canvas")

        more_btn.bind("<Button-1>", more_settings)
        
        more_btn.bind("<Enter>", lambda e: more_btn.config(bg="#f3f4f6"))
        more_btn.bind("<Leave>", lambda e: more_btn.config(bg="white"))

        self.progress_label = Label(self.card, bg="white", fg="#6b7280")
        self.progress_label.pack(anchor="w", pady=(5, 8))

        self.box_container = Frame(self.card, bg="white")
        self.box_container.pack(fill="x")

        self.box_canvas = Canvas(
            self.box_container, 
            bg="white", 
            height=BOX_AREA_HEIGHT, 
            highlightthickness=0
        )
        self.box_canvas.pack(side="left", fill="x", expand=True)

        self.scrollbar = Scrollbar(
            self.box_container, 
            orient="vertical", 
            command=self.box_canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.box_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.box_frame = Frame(self.box_canvas, bg="white")

        self.box_canvas.create_window(
            (0, 0), 
            window=self.box_frame, 
            anchor="nw"
        )

        def update_scroll_region(event=None):
            self.box_canvas.configure(
                scrollregion=self.box_canvas.bbox("all")
            )

        self.box_frame.bind("<Configure>", update_scroll_region)

        def _on_mousewheel(event):
            self.box_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.box_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.load_boxes()

    def delete_goal(self):
        self.dashboard.open_delete_goal_popup(self)
        self.wrapper_more_btn.destroy()
        

    def edit_goal(self):
        self.dashboard.add_goal_popup_edit(self)
        self.wrapper_more_btn.destroy()
        

    def load_boxes(self):
        for w in self.box_frame.winfo_children():
            w.destroy()

        self.box_state = Version2Stage0.get_boxes(self.goal_id)

        checked = sum(self.box_state.values())
        self.progress_label.config(
            text=f"{checked * self.nominal} / {self.target}"
        )

        for i in range(self.total_boxes):
            c = Canvas(
                self.box_frame, 
                width=BOX_SIZE, 
                height=BOX_SIZE, 
                bg="white", 
                highlightthickness=0
            )

            c.grid(row=i // self.COLS, column=i % self.COLS, padx=4, pady=4)

            if self.box_state.get(i, 0):
                c.create_rectangle(
                    4, 4, BOX_SIZE - 4, BOX_SIZE - 4, 
                    fill="#2563eb", 
                    outline="#2563eb"
                )
                c.create_text(
                    BOX_SIZE // 2, 
                    BOX_SIZE // 2, 
                    text="✓", 
                    fill="white"
                )
            else:
                c.create_rectangle(
                    4, 4, BOX_SIZE - 4, BOX_SIZE - 4, 
                    outline="#9ca3af"
                )

            c.bind(
                "<Button-1>", 
                lambda e, idx=i, canvas=c: self.toggle(idx, canvas)
            )

    def toggle(self, index, canvas):
        Version2Stage0.toggle_box(self.goal_id, index)

        current = self.box_state.get(index, 0)
        new_value = 0 if current else 1
        self.box_state[index] = new_value

        canvas.delete("all")

        if new_value:
            canvas.create_rectangle(
                4, 4, BOX_SIZE - 4, BOX_SIZE - 4, 
                fill="#2563eb", 
                outline="#2563eb"
            )
            canvas.create_text(
                BOX_SIZE // 2, 
                BOX_SIZE // 2, 
                text="✓", 
                fill="white"
            )
        else:
            canvas.create_rectangle(
                4, 4, BOX_SIZE - 4, BOX_SIZE - 4, 
                outline="#9ca3af"
            )

        checked = sum(self.box_state.values())
        self.progress_label.config(
            text=f"{checked * self.nominal} / {self.target}"
        )

        delta = self.nominal if new_value else -self.nominal
        self.dashboard.update_total_saved(delta)
