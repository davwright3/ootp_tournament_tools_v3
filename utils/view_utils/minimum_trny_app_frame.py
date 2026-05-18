import tkinter as tk


class MinTrnyAppFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', bd=3)

        self.min_apps_var = tk.StringVar(value='20')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.label = tk.Label(self, text='Min Apps')
        self.label.grid(row=0, column=0, padx=3, pady=3)

        self.min_app_entry = tk.Entry(self, textvariable=self.min_apps_var)
        self.min_app_entry.grid(row=0, column=1, padx=3, pady=3)

    def get_min_apps(self):
        try:
            return int(self.min_app_entry.get())
        except:
            return 20