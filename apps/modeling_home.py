"""Home page for modeling module."""
import tkinter as tk
from apps.batter_modeling import BatterModeling


class ModelingHome(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Modeling Home')
        self.geometry('600x600')

        def open_batter_modeling():
            BatterModeling()

        self.batter_modeling_button = tk.Button(
            self,
            text='Batter Modeling',
            command=open_batter_modeling
        )
        self.batter_modeling_button.grid(row=0, column=0, padx=10, pady=10)


