"""App for recommending lineup settings"""
import tkinter as tk
from utils.view_utils.header_frame import Header
from utils.view_utils.footer_frame import Footer
from utils.stats_utils.build_lineup_from_stats import build_lineup_from_stats
from utils.view_utils.dataframe_table_frame import DataFrameTableFrame


class LineupBuilder(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Lineup Builder")
        self.geometry("1920x1080")

        self.use_dh_var = tk.BooleanVar(value=False)

        def setup_lineup_frames():
            with_dh_list = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF',
                            'DH']
            no_dh_list = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']

            right_widgets = self.set_lineup_v_right_frame.winfo_children()
            for widget in right_widgets:
                widget.destroy()
            left_widgets = self.set_lineup_v_left_frame.winfo_children()
            for widget in left_widgets:
                widget.destroy()

            right_label = tk.Label(self.set_lineup_v_right_frame,
                                   text='Lineup vR')
            right_label.grid(row=0, column=0, sticky="nsew", columnspan=2)

            left_label = tk.Label(self.set_lineup_v_left_frame,
                                  text='Lineup vL')
            left_label.grid(row=0, column=0, sticky="nsew", columnspan=2)

            if self.use_dh_var.get():
                for i in range(len(with_dh_list)):
                    label = tk.Label(
                        self.set_lineup_v_right_frame,
                        text=f'{with_dh_list[i]}: ',
                    )
                    label.grid(row=i + 1, column=0, sticky="nsew", padx=5,
                               pady=5)

                    entry = tk.Entry(self.set_lineup_v_right_frame)
                    entry.grid(row=i + 1, column=1, sticky="nsew", padx=5,
                               pady=5)

                    label = tk.Label(
                        self.set_lineup_v_left_frame,
                        text=f'{with_dh_list[i]}: ',
                    )
                    label.grid(row=i + 1, column=0, sticky="nsew", padx=5,
                               pady=5)

                    entry = tk.Entry(self.set_lineup_v_left_frame)
                    entry.grid(row=i + 1, column=1, sticky="nsew", padx=5,
                               pady=5)
            else:
                for i in range(len(no_dh_list)):
                    label = tk.Label(
                        self.set_lineup_v_right_frame,
                        text=f'{no_dh_list[i]}: ',
                    )
                    label.grid(row=i + 1, column=0, sticky="nsew", padx=5,
                               pady=5)

                    entry = tk.Entry(self.set_lineup_v_right_frame)
                    entry.grid(row=i + 1, column=1, sticky="nsew", padx=5,
                               pady=5)

                    label = tk.Label(
                        self.set_lineup_v_left_frame,
                        text=f'{no_dh_list[i]}: ',
                    )
                    label.grid(row=i + 1, column=0, sticky="nsew", padx=5,
                               pady=5)

                    entry = tk.Entry(self.set_lineup_v_left_frame)
                    entry.grid(row=i + 1, column=1, sticky="nsew", padx=5,
                               pady=5)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = Header(
            self,
            app_name="Lineup Builder",
        )
        self.header_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        self.footer_frame = Footer(
            self
        )
        self.footer_frame.grid(row=2, column=0, sticky="nsew")

        # Set up the main frame
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0)
        self.main_frame.columnconfigure(3, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        self.options_frame = tk.Frame(self.main_frame, relief='groove', bd=3)
        self.options_frame.grid(row=0, column=0, sticky="nsew", columnspan=4)

        self.set_lineup_v_right_frame = tk.Frame(
            self.main_frame, relief='groove', bd=3)
        self.set_lineup_v_right_frame.grid(row=1, column=0, sticky="nsew")

        self.view_lineup_v_right_frame = DataFrameTableFrame(self.main_frame)
        self.view_lineup_v_right_frame.grid(row=1, column=1, sticky="nsew")

        self.set_lineup_v_left_frame = tk.Frame(
            self.main_frame, relief='groove', bd=3)
        self.set_lineup_v_left_frame.grid(row=1, column=2, sticky="nsew")

        self.view_lineup_v_left_frame = DataFrameTableFrame(self.main_frame)
        self.view_lineup_v_left_frame.grid(row=1, column=3, sticky="nsew")

        # Set up the options frame
        self.run_lineups_button = tk.Button(
            self.options_frame,
            text="Run Lineup Builder",
            command=self.build_lineups
        )
        self.run_lineups_button.grid(row=0, column=0, sticky="nsew")

        self.use_dh_button = tk.Checkbutton(
            self.options_frame,
            text="Use DH",
            variable=self.use_dh_var,
            onvalue=True,
            offvalue=False,
            command=setup_lineup_frames
        )
        self.use_dh_button.grid(row=0, column=1, sticky="nsew")

        setup_lineup_frames()

    def build_lineups(self):
        print('Generating lineups')
        # TODO Get the list of players (right and left)
        # TODO Send the list to build lineups method
        # TODO Get a dataframe back that fills in the lineups dynamically
        batters_vs_right_list = []
        batters_vs_left_list = []
        for widget in self.set_lineup_v_right_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                try:
                    cid = widget.get()
                    cid = int(cid)
                except ValueError:
                    cid = 00000
                batters_vs_right_list.append(cid)
        for widget in self.set_lineup_v_left_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                try:
                    cid = widget.get()
                    cid = int(cid)
                except ValueError:
                    cid = 00000
                batters_vs_left_list.append(cid)

        lineup_v_right = build_lineup_from_stats(batters_vs_right_list)
        self.view_lineup_v_right_frame.set_dataframe(lineup_v_right)
        lineup_v_left = build_lineup_from_stats(batters_vs_left_list)
        self.view_lineup_v_left_frame.set_dataframe(lineup_v_left)
