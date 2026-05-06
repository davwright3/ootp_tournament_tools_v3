"""Home page for modeling module."""
import tkinter as tk
from apps.batter_modeling import BatterModeling
from apps.pitcher_modeling import PitcherModeling


class ModelingHome(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Modeling Home')
        self.geometry('600x600')

        def open_batter_modeling():
            BatterModeling()

        def open_pitcher_modeling():
            PitcherModeling()

        self.batter_modeling_button = tk.Button(
            self,
            text='Batter Modeling',
            command=open_batter_modeling
        )
        self.batter_modeling_button.grid(row=0, column=0, padx=10, pady=10)

        self.pitcher_modeling_button = tk.Button(
            self,
            text='Pitcher Modeling',
            command=open_pitcher_modeling
        )
        self.pitcher_modeling_button.grid(row=0, column=1, padx=10, pady=10)


