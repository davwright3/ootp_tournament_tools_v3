"""Module for fitting the current pitching models to the card list."""
from utils.data_utils.card_list_store import card_list_store
from utils.modeling.fit_model import fit_model
from datetime import datetime, timedelta
import pandas as pd


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
        lookback_days=None
        ):
    cards = card_list_store.get_card_list().copy()
    cards = cards[cards['Card Value'].between(min_value, max_value)]
    cards = cards[cards['Year'].between(min_year, max_year)]
    if lookback_days:
        cutoff_date = datetime.today() - timedelta(days=lookback_days)
        cards['date'] = pd.to_datetime(cards['date'], format='%Y-%m-%d')
        cards = cards[cards['date'] >= cutoff_date]
    cards = cards[cards['Card Value'].between(min_value, max_value)]
    cards = cards[cards['Year'].between(min_year, max_year)]

    if name_search is not None:
        print(name_search)
        pattern = '|'.join(name_search)
        cards = cards[cards['//Card Title'].str.contains(pattern, case=False)]

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
        cards = cards[cards['owned'] > 0]

    cards = cards[['//Card Title', 'Card Value', 'Stuff', 'Stuff vL',
                   'Stuff vR', 'pBABIP', 'pBABIP vL', 'pBABIP vR', 'pHR',
                   'pHR vL', 'pHR vR', 'Control', 'Control vL', 'Control vR',
                   'Stamina', 'Throws']]
    cards = fit_model(
        cards,
        'p_babip',
        'P_BABIP_Calc',
        'pit'
    )
    cards = fit_model(
        cards,
        'p_strikeouts',
        'P_Strikeouts_Calc',
        'pit'
    )
    cards = fit_model(
        cards,
        'p_walks',
        'P_Walks_Calc',
        'pit'
    )
    cards = fit_model(
        cards,
        'p_homeruns',
        'P_Homeruns_Calc',
        'pit'
    )

    cards['P_BABIP_Calc'] = round(cards['P_BABIP_Calc'], 3)
    cards['P_Strikeouts_Calc'] = round(cards['P_Strikeouts_Calc'], 3)
    cards['P_Walks_Calc'] = round(cards['P_Walks_Calc'], 3)
    cards['P_Walks_Calc'] = cards['P_Walks_Calc'].clip(lower=0.005)
    cards['Proj BIP'] = 1 - cards['P_Strikeouts_Calc'] - cards['P_Walks_Calc']
    cards['Proj HR'] = round(cards['P_Homeruns_Calc'] * cards['Proj BIP'], 3)
    cards['Proj Net BIP'] = round(cards['Proj BIP'] - cards['Proj HR'], 3)
    cards['Proj Hits'] = round(cards['Proj Net BIP'] * cards['P_BABIP_Calc'],
                               3)
    cards['AVG'] = round((cards['Proj Hits'] + cards['Proj HR']) /
                         (1 - cards['P_Walks_Calc']), 3)
    cards['OBP'] = round(((cards['Proj Hits'] + cards['Proj HR'] +
                           cards['P_Walks_Calc']) / 1), 3)
    cards['TB'] = round(
        (cards['Proj Hits'] * 1.40) + (cards['Proj HR'] * 4), 3)
    cards['SLG'] = round(cards['TB'] / (1 - cards['P_Walks_Calc']), 3)
    cards['OPS'] = round(cards['OBP'] + cards['SLG'], 3)
    cards['Proj HR/600'] = round(cards['Proj HR'] * 600, 1)
    cards['K-BB'] = round(
        cards['P_Strikeouts_Calc'] - cards['P_Walks_Calc'], 3)
    cards['Proj Score'] = round(
        (cards['P_Strikeouts_Calc'] - (cards['P_Walks_Calc'] +
                                       cards['Proj HR'])), 3)

    cards = cards.rename(columns={'//Card Title': 'Title', 'Card Value': 'Val',
                                  'P_BABIP_Calc': 'BABIP',
                                  'P_Strikeouts_Calc': 'K Pct',
                                  'P_Walks_Calc': 'BB Pct',
                                  'Proj Hits': 'Hits',
                                  'Proj HR/600': 'HR/600',
                                  'Proj Score': 'Score'})

    cards = cards[['Title', 'Val', 'BABIP', 'K Pct', 'BB Pct', 'K-BB', 'AVG',
                   'OBP', 'SLG', 'OPS', 'HR/600', 'Score']]

    return cards
