import tkinter as tk


class ThemeTeamAlliterationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', bd=3)

        self.theme_team_only_var = tk.BooleanVar(value=False)

        self.theme_team_checkbox = tk.Checkbutton(self, text='Theme Team Only' ,variable=self.theme_team_only_var, onvalue=True, offvalue=False)
        self.theme_team_checkbox.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')

    def get_theme_team_only_var(self):
        return self.theme_team_only_var.get()