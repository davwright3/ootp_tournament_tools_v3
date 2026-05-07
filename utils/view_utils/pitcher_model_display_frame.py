"""Custom frame for fitting and displaying the pitcher models."""
import tkinter as tk
import json
from datetime import datetime
from utils.modeling.fit_current_pitching_models import fit_current_pitching_models
from utils.config_utils.load_save_settings import get_setting
from utils.view_utils.scrollable_frame import ScrollableFrame
from utils.view_utils.dataframe_table_frame import DataFrameTableFrame
from utils.view_utils.min_max_rating_frame import MinMaxFrame
from utils.view_utils.min_max_years_frame import MinMaxYearsFrame
from utils.view_utils.position_select_frame import PositionSelectFrame
from utils.view_utils.card_type_select_frame import CardTypeSelectFrame
from utils.view_utils.select_in_collection_frame import SelectInCollectionFrame



class PitcherModelDisplayFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        self.babip_model_info = tk.StringVar(value='No data loaded')
        self.babip_model_score_info = tk.StringVar(value='No data loaded')
        self.homerun_model_info = tk.StringVar(value='No data loaded')
        self.homerun_model_score_info = tk.StringVar(value='No data loaded')
        self.strikeout_model_info = tk.StringVar(value='No data loaded')
        self.strikeout_model_score_info = tk.StringVar(value='No data loaded')
        self.walks_model_info = tk.StringVar(value='No data loaded')
        self.walks_model_score_info = tk.StringVar(value='No data loaded')

        self.model_display_frame = DataFrameTableFrame(self)
        self.model_display_frame.grid(row=0, column=0, sticky='nsew')

        self.scrollable_frame = ScrollableFrame(
            self,
            yscroll=True,
            xscroll=False,
            auto_width=False
        )
        self.scrollable_frame.grid(row=0, column=1, sticky='nsew')

        inner = self.scrollable_frame.inner

        self.model_options_frame = tk.Frame(self.scrollable_frame)
        self.model_options_frame.grid(row=0, column=0, sticky='nsew')

        self.fit_models_button = tk.Button(
            self.model_options_frame,
            text='Fit Models',
            command=self.fit_pitching_models
        )
        self.fit_models_button.grid(row=0, column=0, sticky='nsew')

        self.min_max_ratings_frame = MinMaxFrame(
            self.model_options_frame,
        )
        self.min_max_ratings_frame.grid(row=1, column=0, sticky='nsew')

        self.min_max_years_frame = MinMaxYearsFrame(
            self.model_options_frame,
        )
        self.min_max_years_frame.grid(row=2, column=0, sticky='nsew')

        self.position_select_frame = PositionSelectFrame(
            self.model_options_frame,
        )
        self.position_select_frame.grid(row=3, column=0, sticky='nsew')

        self.card_type_select_frame = CardTypeSelectFrame(self.model_options_frame)
        self.card_type_select_frame.grid(row=4, column=0, sticky='nsew')

        self.collection_frame = SelectInCollectionFrame(
            self.model_options_frame,
        )
        self.collection_frame.grid(row=5, column=0, sticky='nsew')

        # Frame for model info
        self.model_info_frame = tk.Frame(self.model_options_frame)
        self.model_info_frame.grid(row=0, column=1, sticky='nsew', rowspan=6)

        self.babip_model_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.babip_model_info
        )
        self.babip_model_info_label.grid(row=0, column=0, sticky='nsew')

        self.babip_model_score_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.babip_model_score_info
        )
        self.babip_model_score_info_label.grid(row=1, column=0, sticky='nsew')

        self.strikeout_model_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.strikeout_model_info
        )
        self.strikeout_model_info_label.grid(row=2, column=0, sticky='nsew')

        self.strikeout_model_score_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.strikeout_model_score_info
        )
        self.strikeout_model_score_info_label.grid(row=3, column=0, sticky='nsew')

        self.walks_model_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.walks_model_info
        )
        self.walks_model_info_label.grid(row=4, column=0, sticky='nsew')

        self.walks_model_score_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.walks_model_score_info
        )
        self.walks_model_score_info_label.grid(row=5, column=0, sticky='nsew')

        self.homerun_model_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.homerun_model_info
        )
        self.homerun_model_info_label.grid(row=6, column=0, sticky='nsew')

        self.homerun_model_score_info_label = tk.Label(
            self.model_info_frame,
            textvariable=self.homerun_model_score_info
        )
        self.homerun_model_score_info_label.grid(row=7, column=0, sticky='nsew')

        self.update_model_info()

    def update_model_info(self):
        target_folder = get_setting('InitialTargetDirs',
                                    'starting_target_folder')
        model_info_path = f'{target_folder}/models/model_tracking.json'

        model_data = json.load(open(model_info_path))

        try:
            pbabip_model_trny = model_data['current_p_babip_tourney_name']
            pbabip_model_type = model_data['current_p_babip']
            pbabip_model_left_score = model_data['current_left_p_babip_score']
            pbabip_model_right_score = model_data['current_right_p_babip_score']
            pbabip_model_date_info = datetime.fromisoformat(model_data['current_babip_runtime'])
            pbabip_model_date = pbabip_model_date_info.strftime("%m/%d %H:%M")

            self.babip_model_info.set(f'pBABIP: {pbabip_model_trny} {pbabip_model_type}')
            self.babip_model_score_info.set(f'{pbabip_model_date} : L: {pbabip_model_left_score} R: {pbabip_model_right_score}')

            pstrikeouts_model_trny = model_data['current_p_strikeouts_tourney_name']
            pstrikeouts_model_type = model_data['current_p_strikeouts']
            pstrikeouts_model_left_score = model_data['current_right_p_strikeouts_score']
            pstrikeouts_model_right_score = model_data['current_left_p_strikeouts_score']
            pstrikeouts_model_date_info = datetime.fromisoformat(model_data['current_p_strikeouts_runtime'])
            pstrikeouts_model_date = pstrikeouts_model_date_info.strftime("%m/%d %H:%M")

            self.strikeout_model_info.set(f'pK: {pstrikeouts_model_trny} {pstrikeouts_model_type}')
            self.strikeout_model_score_info.set(
                (f'{pstrikeouts_model_date} : L: {pstrikeouts_model_left_score}'
                 f' R: {pstrikeouts_model_right_score}'))

            pwalks_model_trny = model_data['current_p_walks_tourney_name']
            pwalks_model_type = model_data['current_p_walks']
            pwalks_model_left_score = model_data['current_left_p_walks_score']
            pwalks_model_right_score = model_data['current_right_p_walks_score']
            pwalks_model_date_info = datetime.fromisoformat(model_data['current_p_walks_runtime'])
            pwalks_model_date = pwalks_model_date_info.strftime("%m/%d %H:%M")

            self.walks_model_info.set(f'pBB: {pwalks_model_trny} {pwalks_model_type}')
            self.walks_model_score_info.set(f'{pwalks_model_date} : L: {pwalks_model_left_score} R: {pwalks_model_right_score}')

            phomeruns_model_trny = model_data['current_p_homeruns_tourney_name']
            phomeruns_model_type = model_data['current_p_homeruns']
            phomeruns_model_left_score = model_data['current_left_p_homeruns_score']
            phomeruns_model_right_score = model_data['current_right_p_homeruns_score']
            phomeruns_model_date_info = datetime.fromisoformat(model_data['current_p_homeruns_runtime'])
            phomeruns_model_date = phomeruns_model_date_info.strftime("%m/%d %H:%M")

            self.homerun_model_info.set(f'pHR: {phomeruns_model_trny} {phomeruns_model_type}')
            self.homerun_model_score_info.set(f'{phomeruns_model_date} : L : {phomeruns_model_left_score} R: {phomeruns_model_right_score}')

        except Exception as e:
            self.babip_model_info.set('pBABIP: No data loaded')
            self.strikeout_model_info.set('pK: No data loaded')
            self.walks_model_info.set('pBB: No data loaded')
            self.homerun_model_info.set('pHR: No data loaded')


    def fit_pitching_models(self):
        print("Fitting pitching models")



