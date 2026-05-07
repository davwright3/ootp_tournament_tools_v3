"""Module for fitting the current pitching models to the card list."""
import pandas as pd
from utils.data_utils.card_list_store import card_list_store


def fit_current_pitching_models(
        cards_df,
        min_value=40,
        max_value=105,
        min_year=1860,
        max_year=2026,
        name_search=None,
        position_select=None,
        pitcher_side_select=None,
        card_type_select=None,
        collection_only=False
    ):
    cards = card_list_store.get_card_list().copy()
    print(cards.head())