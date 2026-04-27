"""
App for modeling outcomes in Perfect Team 27.

Uses scikit learn.
"""

import tkinter as tk
from utils.modeling.run_ridgecv_model_batters import run_ridgecv_model
from utils.view_utils.header_frame import Header
from utils.view_utils.footer_frame import Footer
from utils.data_utils.select_load_stats_data_file import select_load_stats_data_file
from utils.data_utils.card_list_store import card_list_store
from utils.view_utils.model_display_frame import ModelDisplayFrame
from pathlib import Path


class PerfectTeamModeling(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Modeling Perfect Team 27")
        self.geometry("1920x1080")

        self.dataframe_loaded_var = tk.StringVar(value="No file selected.")
        self.is_dataframe_loaded = tk.BooleanVar(value=False)
        self.tourney_name = tk.StringVar(value="None")

        card_list_store.load_card_list()

        def set_active_buttons(frame):
            buttons = []
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Button):
                    buttons.append(widget)

            for button in buttons:
                if self.is_dataframe_loaded.get():
                    button.configure(state=tk.NORMAL)
                else:
                    button.configure(state=tk.DISABLED)

        def set_tourney_name(tourney_path):
            self.tourney_name.set(Path(tourney_path).stem)
            print(self.tourney_name.get())


        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)


        # Main frames for the app
        row = 0

        self.header_frame = Header(self)
        self.header_frame.grid(row=row, column=0, sticky="nsew")
        row += 1

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=row, column=0, sticky="nsew")
        row += 1

        self.footer_frame = Footer(self)
        self.footer_frame.grid(row=row, column=0, sticky="nsew")
        row += 1

        # Set up the main frame
        self.main_frame.columnconfigure(0, weight=1)

        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        main_frame_row = 0
        self.run_model_frame = tk.Frame(self.main_frame)
        self.run_model_frame.grid(row=main_frame_row, column=0, sticky="nsew")
        main_frame_row += 1

        self.view_model_frame = ModelDisplayFrame(self.main_frame)
        self.view_model_frame.grid(row=main_frame_row, column=0, sticky="nsew")
        main_frame_row += 1

        # Set up the run model frame and buttons
        run_model_frame_row = 0

        self.file_select_button = tk.Button(
            self.run_model_frame,
            text="Select File",
            state=tk.NORMAL,
            command=lambda: (
                select_load_stats_data_file(
                    self,
                    loaded_file_var=self.dataframe_loaded_var,
                    file_loaded_bool=self.is_dataframe_loaded,
                ),
                set_active_buttons(self.run_model_buttons_frame),
                set_tourney_name(self.dataframe_loaded_var.get()),
            )
        )
        self.file_select_button.grid(row=run_model_frame_row, column=0, sticky="w")

        self.selected_file_label = tk.Label(
            self.run_model_frame,
            textvariable=self.dataframe_loaded_var
        )
        self.selected_file_label.grid(row=run_model_frame_row, column=1, sticky="w")
        run_model_frame_row += 1


        self.run_model_buttons_frame = tk.Frame(self.run_model_frame)
        self.run_model_buttons_frame.grid(
            row=run_model_frame_row,
            column=0,
            sticky="nsew"
        )

        # Modeling buttons
        model_button_frame_column = 0
        model_button_frame_row = 0
        self.ridge_models_label = tk.Label(
            self.run_model_buttons_frame,
            text="Ridge Models"
        )
        self.ridge_models_label.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="w")
        model_button_frame_column += 1

        self.model_babip_button = tk.Button(
            self.run_model_buttons_frame,
            text='Run BABIP Model',
            command=self.run_babip_model
        )
        self.model_babip_button.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="nsew")
        model_button_frame_column += 1

        self.model_strikeouts_button = tk.Button(
            self.run_model_buttons_frame,
            text='Run Strikeout Model',
            command=self.run_strikeout_model
        )
        self.model_strikeouts_button.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="nsew")
        model_button_frame_column += 1

        self.model_walks_button = tk.Button(
            self.run_model_buttons_frame,
            text='Run Walks Model',
            command=self.run_walks_model
        )
        self.model_walks_button.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="nsew")
        model_button_frame_column += 1

        self.model_home_runs_button = tk.Button(
            self.run_model_buttons_frame,
            text='Run HR Model',
            command=self.run_homeruns_model
        )
        self.model_home_runs_button.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="nsew")
        model_button_frame_column += 1

        self.model_xbh_button = tk.Button(
            self.run_model_buttons_frame,
            text='Run XBH Model',
            command=self.run_xbh_model
        )
        self.model_xbh_button.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="nsew")
        model_button_frame_column += 1

        self.all_models_button = tk.Button(
            self.run_model_buttons_frame,
            text='Run All Models',
            command=self.run_all_ridge_models
        )
        self.all_models_button.grid(row=run_model_frame_row, column=model_button_frame_column, sticky="nsew")
        model_button_frame_column += 1
        run_model_frame_row += 1

        # End run model frame


        set_active_buttons(self.run_model_buttons_frame)

    def run_babip_model(self):
        run_ridgecv_model(
            passed_stat_columns=['CID', 'PA', 'AB', 'H', 'HR', 'K', 'SF'],
            passed_card_columns=['Card ID', '//Card Title', 'BABIP',
                                 'BABIP vL',
                                 'BABIP vR', 'Speed', 'BattedBallType',
                                 'Bats'],
            model_calc_name='babip',
            target_name='BABIP Calc',
            model_headers=['BABIP', 'BABIP vL', 'BABIP vR', 'Speed'],
            alpha_params=[0.1, 1, 10, 100],
            cv_params=3,
            trny_name=self.tourney_name.get()
        ),
        self.view_model_frame.update_model_info_display()

    def run_strikeout_model(self):
        run_ridgecv_model(
            passed_stat_columns=['CID', 'PA', 'K'],
            passed_card_columns=['Card ID', '//Card Title', 'Avoid Ks',
                                 'Avoid K vL', 'Avoid K vR', 'Eye', 'Eye vL',
                                 'Eye vR', 'BattedBallType', 'Bats'],
            model_calc_name='strikeouts',
            target_name='Strikeout Calc',
            model_headers=['Avoid Ks', 'Avoid K vL', 'Avoid K vR'],
            alpha_params=[0.1, 1, 10, 100],
            cv_params=3,
            trny_name=self.tourney_name.get()
        ),
        self.view_model_frame.update_model_info_display()

    def run_walks_model(self):
        run_ridgecv_model(
            passed_stat_columns=['CID', 'PA', 'BB'],
            passed_card_columns=['Card ID', '//Card Title', 'Avoid Ks',
                                 'Avoid K vL', 'Avoid K vR', 'Eye', 'Eye vL',
                                 'Eye vR', 'BattedBallType', 'Bats'],
            model_calc_name='walks',
            target_name='Walk Calc',
            model_headers=['Eye', 'Eye vL', 'Eye vR'],
            alpha_params=[0.1, 1, 10, 100],
            cv_params=3,
            trny_name=self.tourney_name.get()
        ),
        self.view_model_frame.update_model_info_display()

    def run_homeruns_model(self):
        run_ridgecv_model(
            passed_stat_columns=['CID', 'PA', 'AB', 'K', 'BB', 'HP', 'IBB',
                                 'HR'],
            passed_card_columns=['Card ID', '//Card Title', 'Power',
                                 'Power vL',
                                 'Power vR', 'BattedBallType', 'Bats'],
            model_calc_name='homeruns',
            target_name='HR Calc',
            model_headers=['Power', 'Power vL', 'Power vR'],
            alpha_params=[0.1, 1, 10, 100],
            cv_params=3,
            trny_name=self.tourney_name.get()
        ),
        self.view_model_frame.update_model_info_display()

    def run_xbh_model(self):
        run_ridgecv_model(
            passed_stat_columns=['CID', 'PA', 'H', '2B', '3B'],
            passed_card_columns=['Card ID', '//Card Title', 'Gap', 'Gap vL',
                                 'Gap vR',
                                 'Baserunning', 'Speed', 'Bats'],
            model_calc_name='xbh',
            target_name='XBH Calc',
            model_headers=['Gap', 'Gap vL', 'Gap vR', 'Baserunning', 'Speed'],
            alpha_params=[0.1, 1, 10, 100],
            cv_params=3,
            trny_name=self.tourney_name.get()
        ),
        self.view_model_frame.update_model_info_display()

    def run_all_ridge_models(self):
        self.run_babip_model(),
        self.run_strikeout_model(),
        self.run_walks_model(),
        self.run_homeruns_model(),
        self.run_xbh_model(),
        self.view_model_frame.update_model_info_display()

