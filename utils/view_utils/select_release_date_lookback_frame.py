"""Module for cutting cards by release date in days previous."""
import tkinter as tk


class SelectReleaseDateFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lookback_days_var = tk.StringVar(value=None)

        self.label = tk.Label(self, text="Release Window")
        self.label.grid(column=0, row=0, sticky='nsew', padx=3, pady=3)

        self.entry = tk.Entry(self, textvariable=self.lookback_days_var)
        self.entry.grid(column=1, row=0, sticky='nsew', padx=3, pady=3)

    def get_lookback_days(self):
        try:
            lookback_days = int(self.entry.get())
        except ValueError:
            lookback_days = None

        return lookback_days
