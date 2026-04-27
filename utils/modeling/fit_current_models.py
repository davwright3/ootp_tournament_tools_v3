"""Utility for fitting currently stored models for display."""
from utils.config_utils.load_save_settings import get_setting
from utils.data_utils.card_list_store import card_list_store

def fit_current_models(
        min_value=40,
        max_value=105,
        min_year=1860,
        max_year=2026,
        position_select=None,
        batter_side_select=None,
        card_type_select=None,
):
    print("Fitting current models...")
    target_folder = get_setting("IntialTargetDirs", 'starting_target_folder')

    cards = card_list_store.get_card_list().copy()
    cards = cards[cards['Card Value'].between(min_value, max_value)]
    cards = cards[cards['Year'].between(min_year, max_year)]

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

    print(cards.head())
