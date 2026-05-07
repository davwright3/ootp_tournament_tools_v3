import tkinter as tk


class ViewBattersFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', bd=3)

        self.use_batters_var = tk.BooleanVar(value=False)

        self.use_batters_select = tk.Checkbutton(
            self,
            text='View Batters',
            variable=self.use_batters_var,
            onvalue=True,
            offvalue=False,
        )
        self.use_batters_select.grid(row=0, column=0, sticky='nsew')

    def get_use_batters(self):
        return self.use_batters_var.get()