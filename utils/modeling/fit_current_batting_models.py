"""Utility for fitting currently stored models for display."""
import pandas as pd
import numpy as np
import joblib
from utils.modeling.fit_batters_babip_model import fit_batters_babip_model
from utils.config_utils.load_save_settings import get_setting
from utils.data_utils.card_list_store import card_list_store

def fit_current_models(
        min_value=40,
        max_value=105,
        min_year=1860,
        max_year=2026,
        name_search=None,
        position_select=None,
        batter_side_select=None,
        card_type_select=None,
):
    print("Fitting current models...")
    target_folder = get_setting("IntialTargetDirs", 'starting_target_folder')

    cards = card_list_store.get_card_list().copy()
    cards = cards[['Card ID', '//Card Title', 'Card Value', 'Year', 'Bats',
                   'Card Type', 'BABIP', 'BABIP vL', 'BABIP vR', 'Avoid Ks',
                   'Avoid K vL', 'Avoid K vR', 'Power', 'Power vL', 'Power vR',
                   'Gap', 'Gap vL', 'Gap vR', 'Eye', 'Eye vL', 'Eye vR',
                   'BattedBallType', 'Speed', 'Baserunning']]
    cards = cards[cards['Card Value'].between(min_value, max_value)]
    cards = cards[cards['Year'].between(min_year, max_year)]

    if name_search is not None:
        cards = cards[cards['//Card Title'].str.contains(name_search, case=False, na=False)]

    if position_select is not None:
        cards = cards[cards[position_select] == 1]

    if batter_side_select != 'All':
        if batter_side_select == 'L':
            selected_side = 1
        elif batter_side_select == 'R':
            selected_side = 2
        else:
            selected_side = 3
        cards = cards[cards['Bats'] == selected_side]

    if card_type_select is not None:
        cards = cards[cards['Card Type'].isin(card_type_select)]

    cards = fit_batters_babip_model(cards)


    print(cards.head())
