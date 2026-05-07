"""Module for fitting the current pitching models to the card list."""
import pandas as pd
from utils.data_utils.card_list_store import card_list_store
from utils.modeling.fit_model import fit_model


def fit_current_pitching_models(
        min_value=40,
        max_value=105,
        min_year=1860,
        max_year=2026,
        name_search=None,
        position_select=None,
        pitcher_side_select=None,
        card_type_select=None,
        collection_only=False,
        view_batters=False,
        pitcher_type=None,
    ):
    cards = card_list_store.get_card_list().copy()
    cards = cards[cards['Card Value'].between(min_value, max_value)]
    cards = cards[cards['Year'].between(min_year, max_year)]


    if name_search is not None:
        cards = cards[cards['Name'].str.contains(name_search)]

    if pitcher_side_select != 'All':
        if pitcher_side_select == 'R':
            pitcher_side_select = 1
        else:
            pitcher_side_select = 2
        cards = cards[cards['Throws'] == pitcher_side_select]


    if card_type_select is not None:
        cards = cards[cards['Card Type'].isin(card_type_select)]

    if view_batters:
        if position_select is not None:
            cards = cards[cards[position_select] == 1]
    elif pitcher_type is not None:
        if pitcher_type == 'SP':
            cards = cards[cards['Pitcher Role'] == 11]
        else:
            cards = cards[cards['Pitcher Role'].isin([12, 13])]
    else:
        cards = cards[cards['Position'] == 1]

    if collection_only is True:
        cards = cards[cards['onhand'] > 0]

    cards = cards[['//Card Title', 'Card Value', 'Stuff', 'Stuff vL',
                   'Stuff vR', 'pBABIP', 'pBABIP vL', 'pBABIP vR', 'pHR',
                   'pHR vL', 'pHR vR', 'Control', 'Control vL', 'Control vR',
                   'Stamina', 'Throws']]
    cards = fit_model(cards, 'p_babip', 'P_BABIP_Calc', 'pit')
    cards = fit_model(cards, 'p_strikeouts', 'P_Strikeouts_Calc', 'pit')
    cards = fit_model(cards, 'p_walks', 'P_Walks_Calc', 'pit')
    cards = fit_model(cards, 'p_homeruns', 'P_Homeruns_Calc', 'pit')

    return cards

