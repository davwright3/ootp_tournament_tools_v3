"""App for running and viewing pitcher models for PT 27."""
import tkinter as tk
from pathlib import Path
from utils.view_utils.header_frame import Header
from utils.view_utils.footer_frame import Footer
from utils.data_utils.select_load_stats_data_file import select_load_stats_data_file
from utils.modeling.run_model import run_ridgecv_model
from utils.view_utils.pitcher_model_ratings_select_frame import PitcherModelRatingsFrame
from utils.view_utils.model_params_frame import ModelParametersFrame


class PitcherModeling(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.geometry("1920x1080")

        self.is_dataframe_loaded = tk.BooleanVar(value=False)
        self.loaded_file = tk.StringVar(value='No file selected')
        self.tourney_name = tk.StringVar(value='None selected')

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

        self.header_frame = Header(self, app_name='Pitcher Modeling')
        self.header_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        self.footer_frame = Footer(self)
        self.footer_frame.grid(row=2, column=0, sticky="nsew")

        # Set up main frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        self.run_model_frame = tk.Frame(self.main_frame)
        self.run_model_frame.grid(row=0, column=0, sticky="nsew")

        self.display_model_frame = tk.Frame(self.main_frame)
        self.display_model_frame.grid(row=1, column=0, sticky="nsew")

        # Set up the frame for running models
        self.select_file_button = tk.Button(
            self.run_model_frame,
            text="Select File",
            command=lambda: (select_load_stats_data_file(
                self.run_model_frame,
                loaded_file_var=self.loaded_file,
                file_loaded_bool=self.is_dataframe_loaded,
            ),
                set_active_buttons(self.run_model_buttons_frame),
                set_tourney_name(self.loaded_file.get()),
            )
        )
        self.select_file_button.grid(row=0, column=0, sticky="nsew")

        self.selected_file_label = tk.Label(self.run_model_frame, textvariable=self.loaded_file)
        self.selected_file_label.grid(row=0, column=1, sticky="nsew")

        self.run_model_buttons_frame = tk.Frame(self.run_model_frame)
        self.run_model_buttons_frame.grid(row=1, column=0, sticky="nsew")

        self.run_pitcher_strikeouts_model_button = tk.Button(
            self.run_model_buttons_frame,
            text="Run Pitcher Model",
            command=lambda: self.run_pitcher_model(
                ['Stuff', 'Stuff vL', 'Stuff vR'],
                ['CID', 'IP', 'K_1', 'BF'],
                'p_strikeouts',
                'P_K_Calc'
            )
        )
        self.run_pitcher_strikeouts_model_button.grid(row=0, column=0, sticky="nsew")

        self.ratings_select_frame = PitcherModelRatingsFrame(self.run_model_frame)
        self.ratings_select_frame.grid(row=0, column=2, sticky="nsew", rowspan=2)

        self.model_parameters_frame = ModelParametersFrame(self.run_model_frame)
        self.model_parameters_frame.grid(row=0, column=3, sticky="nsew", rowspan=2)

        set_active_buttons(self.run_model_buttons_frame)


    def run_pitcher_model(
            self,
            default_ratings,
            stat_columns,
            model_name,
            target_name
    ):
        selected_ratings = self.ratings_select_frame.get_active_ratings()
        if len(selected_ratings) == 0:
            selected_ratings = default_ratings
        columns = ['Card ID', '//Card Title', 'Throws']
        columns.extend(selected_ratings)
        alphas, cv_set, set_test_size, model_type = self.model_parameters_frame.get_params()
        print(columns)

        run_ridgecv_model(
            passed_stat_columns=stat_columns,
            passed_card_columns=columns,
            model_calc_name=model_name,
            target_name=target_name,
            model_headers=selected_ratings,
            alpha_params=alphas,
            cv_params=cv_set,
            test_size=set_test_size,
            player_type='pit',
            model_type=model_type,
            use_batted_ball_type=False,
            trny_name=self.tourney_name.get()
        )




