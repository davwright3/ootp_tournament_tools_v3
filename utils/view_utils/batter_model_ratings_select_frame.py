"""Custom frame for selecting batter ratings to use in modeling app."""
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkCheckBox


class BatterModelRatingsSelectFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label = tk.Label(self, text="Ratings Select")
        self.label.grid(row=0, column=0, padx=10, pady=10, columnspan=7)

        self.batter_ratings_list = ['BABIP', 'BABIP vL', 'BABIP vR', 'Avoid Ks',
                               'Avoid K vL', 'Avoid K vR', 'Gap', 'Gap vL',
                               'Gap vR', 'Power', 'Power vL', 'Power vR',
                               'Eye', 'Eye vL', 'Eye vR', 'Speed',
                                'Baserunning', 'Steal Rate', 'Stealing'
                               ]

        self.selected_ratings = []
        self.use_batted_ball_type = tk.BooleanVar(value=False)

        def set_active_stats():
            self.selected_ratings.clear()
            for child in self.winfo_children():
                if isinstance(child, CTkCheckBox):
                    if child.get() != 'off':
                        self.selected_ratings.append(child.get())

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        item = 0
        for rating in self.batter_ratings_list:
            checkbox = ctk.CTkCheckBox(
                self,
                text=rating,
                onvalue=rating,
                offvalue='off',
                command=set_active_stats
            )
            checkbox.grid(row=item // 6 + 1, column=item % 6, padx=1, pady=1)
            item += 1

        self.use_batted_ball_type_checkbox = tk.Checkbutton(
            self,
            text='Use Batted Ball Type',
            variable=self.use_batted_ball_type,
            onvalue=True,
            offvalue=False,
        )
        self.use_batted_ball_type_checkbox.grid(row=1, column=6)

    def get_selected_ratings(self):
        return self.selected_ratings

    def get_use_bbt(self):
        return self.use_batted_ball_type.get()

