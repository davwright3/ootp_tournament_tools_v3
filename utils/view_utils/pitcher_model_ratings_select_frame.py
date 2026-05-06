"""Frame for selecting ratings for pitcher model."""
import tkinter as tk
import customtkinter as ctk


class PitcherModelRatingsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.ratings_list = ['Stuff', 'Stuff vL', 'Stuff vR', 'pHR', 'pHR vL',
                        'pHR vR', 'pBABIP', 'pBABIP vL', 'pBABIP vR',
                        'Control', 'Control vL', 'Control vR']

        self.selected_ratings_list = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        def set_active_ratings():
            self.selected_ratings_list.clear()
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkCheckBox):
                    if child.get() != 0:
                        self.selected_ratings_list.append(child.get())

        item = 0
        for rating in self.ratings_list:
            checkbox = ctk.CTkCheckBox(
                self,
                text=rating,
                onvalue=rating,
                offvalue=0,
                command=set_active_ratings
            )
            checkbox.grid(row=item // 3 + 1, column=item % 3, sticky='nsew')
            item += 1

    def get_active_ratings(self):
        return self.selected_ratings_list

