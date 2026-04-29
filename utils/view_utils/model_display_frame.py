"""
Frame for displaying model data.
To be used with the model app.
"""
import tkinter as tk

from utils.modeling.fit_current_batting_models import fit_current_models
from utils.view_utils.position_select_frame import PositionSelectFrame
from utils.view_utils.search_frame import SearchFrame
from utils.view_utils.min_max_rating_frame import MinMaxFrame
from utils.view_utils.min_max_years_frame import MinMaxYearsFrame
from utils.view_utils.card_type_select_frame import CardTypeSelectFrame
from utils.view_utils.batting_side_select_frame import BattingSideSelectFrame
from utils.config_utils.load_save_settings import get_setting
from utils.modeling.fit_current_batting_models import fit_current_models
import json
from datetime import datetime
from pathlib import Path



class ModelDisplayFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='light blue', relief='groove', bd=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

        self.babip_model_info = tk.StringVar(value='No Info Available')
        self.strikeout_model_info = tk.StringVar(value='No Info Available')
        self.walk_model_info = tk.StringVar(value='No Info Available')
        self.homerun_model_info = tk.StringVar(value='No Info Available')
        self.xbh_model_info = tk.StringVar(value='No Info Available')

        # Main frame for viewing data
        self.view_model_results_frame = tk.Frame(self)
        self.view_model_results_frame.grid(row=0, column=0, sticky="nsew")

        # Frame for options
        self.options_frame = tk.Frame(self)
        self.options_frame.grid(row=0, column=1, sticky="nsew")

        options_frame_row = 0
        self.run_model_button = tk.Button(self.options_frame, text="Run Model", command=self.run_model)
        self.run_model_button.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        self.player_search_input = SearchFrame(self.options_frame)
        self.player_search_input.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        self.min_max_value_frame = MinMaxFrame(self.options_frame)
        self.min_max_value_frame.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        self.min_max_years_frame = MinMaxYearsFrame(self.options_frame)
        self.min_max_years_frame.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        self.position_select_frame = PositionSelectFrame(self.options_frame)
        self.position_select_frame.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        self.batting_side_select_frame = BattingSideSelectFrame(self.options_frame)
        self.batting_side_select_frame.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        self.card_type_select_frame = CardTypeSelectFrame(self.options_frame)
        self.card_type_select_frame.grid(row=options_frame_row, column=0, sticky="nsew")
        options_frame_row += 1

        # Frame for seeing model data
        self.model_info_frame = tk.Frame(self)
        self.model_info_frame.grid(row=0, column=2, sticky="nsew")

        model_info_frame_row = 0

        self.babip_model_info_name = tk.Label(self.model_info_frame, text="BABIP Model")
        self.babip_model_info_name.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.babip_model_info_label = tk.Label(self.model_info_frame, textvariable=self.babip_model_info)
        self.babip_model_info_label.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.strikeout_model_info_name = tk.Label(self.model_info_frame, text="Strikeout Model")
        self.strikeout_model_info_name.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.strikeout_model_info_label = tk.Label(self.model_info_frame, textvariable=self.strikeout_model_info)
        self.strikeout_model_info_label.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.walk_model_info_name = tk.Label(self.model_info_frame, text="Walk Model")
        self.walk_model_info_name.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.walk_model_info_label = tk.Label(self.model_info_frame, textvariable=self.walk_model_info)
        self.walk_model_info_label.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.homerun_model_info_name = tk.Label(self.model_info_frame, text="Home Run Model")
        self.homerun_model_info_name.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.homerun_model_info_label = tk.Label(self.model_info_frame, textvariable=self.homerun_model_info)
        self.homerun_model_info_label.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.xbh_model_info_name = tk.Label(self.model_info_frame, text="XBH Model")
        self.xbh_model_info_name.grid(row=model_info_frame_row, column=0, sticky="nsew")
        model_info_frame_row += 1

        self.xbh_model_info_label = tk.Label(self.model_info_frame, textvariable=self.xbh_model_info)
        self.xbh_model_info_label.grid(row=model_info_frame_row, column=0, sticky="nsew")


        self.update_model_info_display()

    def run_model(self):
        min_rating, max_rating = self.min_max_value_frame.get_min_max_rating()
        selected_min_year, selected_max_year = self.min_max_years_frame.get_min_max_years()
        selected_search_name = self.player_search_input.get_search_term()
        selected_position = self.position_select_frame.get_position_select()
        selected_batter_side = self.batting_side_select_frame.get_selected_side()
        selected_card_type = self.card_type_select_frame.get_selected_card_types()

        fit_current_models(
            min_value=min_rating,
            max_value=max_rating,
            min_year=selected_min_year,
            max_year=selected_max_year,
            name_search=selected_search_name,
            position_select=selected_position,
            batter_side_select=selected_batter_side,
            card_type_select=selected_card_type,
        )

    def update_model_info_display(self):
        target_folder = get_setting('InitialTargetDirs', 'starting_target_folder')
        model_info_path = f'{target_folder}/models/model_tracking.json'

        model_data = json.load(open(model_info_path))

        babip_model_trny = model_data['current_babip_tourney_name']
        babip_model_type = model_data['current_babip']
        babip_model_date_info = datetime.fromisoformat(model_data['current_babip_runtime'])
        babip_model_datetime = babip_model_date_info.strftime("%m/%d/%Y %H:%M:%S")

        babip_model_data = f'{babip_model_trny} {babip_model_type} : {babip_model_datetime}'
        self.babip_model_info.set(babip_model_data)

        strikeout_model_trny = model_data['current_strikeouts_tourney_name']
        strikeout_model_type = model_data['current_strikeouts']
        strikeout_model_date_info = datetime.fromisoformat(model_data['current_strikeouts_runtime'])
        strikeout_model_datetime = strikeout_model_date_info.strftime("%m/%d/%Y %H:%M:%S")

        strikeout_model_data = f'{strikeout_model_trny} {strikeout_model_type} : {strikeout_model_datetime}'
        self.strikeout_model_info.set(strikeout_model_data)

        walk_model_trny = model_data['current_walks_tourney_name']
        walk_model_type = model_data['current_walks']
        walk_model_date_info = datetime.fromisoformat(model_data['current_walks_runtime'])
        walk_model_datetime = walk_model_date_info.strftime("%m/%d/%Y %H:%M:%S")

        walk_model_data = f'{walk_model_trny} {walk_model_type} : {walk_model_datetime}'
        self.walk_model_info.set(walk_model_data)

        homerun_model_trny = model_data['current_homeruns_tourney_name']
        homerun_model_type = model_data['current_homeruns']
        home_model_date_info = datetime.fromisoformat(model_data['current_homeruns_runtime'])
        home_model_datetime = home_model_date_info.strftime("%m/%d/%Y %H:%M:%S")

        homerun_model_data = f'{homerun_model_trny} {homerun_model_type} : {home_model_datetime}'
        self.homerun_model_info.set(homerun_model_data)

        xbh_model_trny = model_data['current_xbh_tourney_name']
        xbh_model_type = model_data['current_xbh']
        xbh_model_date_info = datetime.fromisoformat(model_data['current_xbh_runtime'])
        xbh_model_datetime = xbh_model_date_info.strftime("%m/%d/%Y %H:%M:%S")

        xbh_model_data = f'{xbh_model_trny} {xbh_model_type} : {xbh_model_datetime}'
        self.xbh_model_info.set(xbh_model_data)
