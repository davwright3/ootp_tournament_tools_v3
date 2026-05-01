"""Utility for fitting currently stored models for display."""
from utils.modeling.fit_batters_model import fit_batters_model
from utils.data_utils.card_list_store import card_list_store
import pandas as pd

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
    cards = card_list_store.get_card_list().copy()
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

    cards['CD'] = cards['CatcherAbil'] + cards['CatcherFrame'] + cards['Catcher Arm']
    cards['IFD'] = cards['Infield Range'] + cards['Infield Error'] + cards['Infield Arm'] + cards['DP']
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

    cards = fit_batters_model(cards, 'babip', 'BABIP_pred')
    cards['BABIP_pred'] = cards['BABIP_pred'].clip(lower=0)
    cards = fit_batters_model(cards, 'strikeouts', 'K_pred')
    cards['K_pred'] = cards['K_pred'].clip(lower=0)
    cards = fit_batters_model(cards, 'walks', 'BB_pred')
    cards['BB_pred'] = cards['BB_pred'].clip(lower=0)
    cards = fit_batters_model(cards, 'homeruns', 'HR_pred')
    cards['HR_pred'] = cards['HR_pred'].clip(lower=0)
    cards = fit_batters_model(cards, 'xbh', 'XBH_pred')
    cards['XBH_pred'] = cards['XBH_pred'].clip(lower=0)

    cards['K/600'] = round(cards['K_pred'] * 600, 2)
    cards['BB/600'] = round(cards['BB_pred'] * 600, 2)
    cards['tBIP'] = 600 - cards['K/600'] - cards['BB/600']
    cards['HR/600'] = round(cards['tBIP'] * cards['HR_pred'], 2)
    cards['nBIP'] = cards['tBIP'] - cards['HR/600']
    cards['nHits'] = round(cards['nBIP'] * cards['BABIP_pred'], 1)
    cards['XBH/600'] = cards['nHits'] * cards['XBH_pred']
    cards['2B/600'] = round(cards['XBH/600'] * .85, 2)
    cards['3B/600'] = round(cards['XBH/600'] * .15, 2)
    cards['1B/600'] = round(cards['nHits'] - cards['XBH/600'], 2)
    cards['AVG'] = round((cards['nHits'] + cards['HR/600']) / (600 - cards['BB/600']), 3)
    cards['OBP'] = round((cards['nHits'] + cards['HR/600'] + cards['BB/600'] + 4) / 600, 3)
    cards['SLG'] = round((cards['1B/600'] + (cards['2B/600'] * 2) + (cards['3B/600'] * 3) + (cards['HR/600'] * 4)) / (600 - cards['BB/600']), 3)
    cards['OPS'] = round(cards['OBP'] + cards['SLG'], 3)
    cards['wOBA'] = round(((cards['BB/600'] * .701) + (4 * .722) + (cards['1B/600'] * .895) + (cards['2B/600'] * 1.270) + (cards['3B/600'] * 1.608) + (cards['HR/600'] * 2.072)) / (600 - 12), 3)

    final_df = cards[['//Card Title', 'Card Value', 'HR/600', 'AVG', 'OBP', 'SLG', 'OPS', 'wOBA', 'K/600', 'BB/600', 'CD', 'IFD', 'OFD']]
    return final_df




