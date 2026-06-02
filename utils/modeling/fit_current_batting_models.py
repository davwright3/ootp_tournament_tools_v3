"""Utility for fitting currently stored models for display."""
from utils.data_utils.card_list_store import card_list_store
import pandas as pd
from utils.modeling.fit_batter_models import fit_batter_model
from datetime import datetime, timedelta


def fit_current_batting_models(
        min_value=40,
        max_value=105,
        min_year=1860,
        max_year=2026,
        name_search=None,
        lookback_days=None,
        position_select=None,
        batter_side_select=None,
        card_type_select=None,
        collection_only=False
):
    cards = card_list_store.get_card_list().copy()
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

    if collection_only:
        cards = cards[cards['owned'] != 0]

    if position_select is not None:
        cards = cards[cards[position_select] == 1]

    if batter_side_select != 'All':
        if batter_side_select == 'L':
            selected_side = 2
        elif batter_side_select == 'R':
            selected_side = 1
        else:
            selected_side = 3
        cards = cards[cards['Bats'] == selected_side]

    if card_type_select is not None:
        cards = cards[cards['Card Type'].isin(card_type_select)]

    cards['CD'] = (cards['CatcherAbil'] +
                   cards['CatcherFrame'] + cards['Catcher Arm'])
    cards['IFD'] = (cards['Infield Range'] + cards['Infield Error'] +
                    cards['Infield Arm'] + cards['DP'])
    cards['OFD'] = cards['OF Range'] + cards['OF Error'] + cards['OF Arm']

    cards = cards[['Card ID', '//Card Title', 'Card Value', 'Year', 'Bats',
                   'Card Type', 'BABIP', 'BABIP vL', 'BABIP vR', 'Avoid Ks',
                   'Avoid K vL', 'Avoid K vR', 'Power', 'Power vL', 'Power vR',
                   'Gap', 'Gap vL', 'Gap vR', 'Eye', 'Eye vL', 'Eye vR',
                   'BattedBallType', 'Speed', 'Baserunning', 'Steal Rate',
                   'Stealing', 'CD', 'IFD', 'OFD']]
    cards['BattedBallType'] = cards['BattedBallType'].map(
        {0: 'N', 1: 'GB', 2: 'FB', 3: 'LD'})
    cards = pd.get_dummies(cards, columns=['BattedBallType'], drop_first=False)

    cards = fit_batter_model(cards)

    final_df = cards[['//Card Title', 'Card Value', 'HR/600', 'AVG', 'OBP',
                      'SLG', 'OPS', 'wOBA', 'K/600', 'BB/600', 'CD',
                      'IFD', 'OFD']]
    return final_df
