import tkinter as tk


class PitcherRoleSelectFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', bd= 3)

        self.pitcher_role = tk.StringVar(value='Any')
        self.min_stamina = tk.StringVar(value='0')

        self.columnconfigure(0, weight=1)

        self.role_frame = tk.Frame(self)
        self.role_frame.grid(row=0, column=0, sticky='nsew')

        self.role_frame.columnconfigure(0, weight=1)
        self.role_frame.columnconfigure(1, weight=1)
        self.role_frame.columnconfigure(2, weight=1)
        self.role_frame.columnconfigure(3, weight=1)

        self.role_label = tk.Label(self.role_frame, text='Pitcher Role: ')
        self.role_label.grid(row=0, column=0, sticky='nsew')

        self.any_radio = tk.Radiobutton(
            self.role_frame,
            text='Any',
            variable=self.pitcher_role,
            value='Any',
        )
        self.any_radio.grid(row=0, column=1, sticky='nsew')

        self.starter_radio = tk.Radiobutton(
            self.role_frame,
            text='SP',
            variable=self.pitcher_role,
            value='SP',
        )
        self.starter_radio.grid(row=0, column=2, sticky='nsew')

        self.reliever_radio = tk.Radiobutton(
            self.role_frame,
            text='RP',
            variable=self.pitcher_role,
            value='RP',
        )
        self.reliever_radio.grid(row=0, column=3, sticky='nsew')

        self.stamina_frame = tk.Frame(self)
        self.stamina_frame.grid(row=1, column=0, sticky='nsew')
        self.stamina_frame.columnconfigure(0, weight=1)
        self.stamina_frame.columnconfigure(1, weight=1)

        self.stamina_label = tk.Label(self.stamina_frame, text='Min Stamina: ')
        self.stamina_label.grid(row=0, column=0, sticky='nsew')

        self.min_stamina_entry = tk.Entry(
            self.stamina_frame,
            textvariable=self.min_stamina,
        )
        self.min_stamina_entry.grid(row=0, column=1, sticky='nsew')


    def get_pitcher_role(self):
        try:
            min_stamina = int(self.min_stamina.get())
        except ValueError:
            min_stamina = None

        return self.pitcher_role.get(), min_stamina


