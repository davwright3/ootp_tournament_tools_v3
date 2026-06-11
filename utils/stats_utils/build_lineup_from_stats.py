"""Script for building a lineup from a list of players and their stats."""
import pandas as pd
from utils.data_utils.data_store import data_store
from utils.data_utils.card_list_store import card_list_store
from utils.stats_utils.cull_teams import cull_teams
from utils.stats_utils.calc_batting_stats import calc_batting_stats
import logging

logger = logging.getLogger('apps.basic_stats_app')


def build_lineup_from_stats(player_list=None):
    stats = cull_teams(data_store.get_data().copy())

    cards = card_list_store.get_card_list().copy()[['Card ID',
                                                    'FirstName', 'LastName']]
    cards = cards.rename(columns={'Card ID': 'CID'})
    cards['Name'] = cards['FirstName'] + ' ' + cards['LastName']
    cards = cards[cards['CID'].isin(player_list)]

    stats = stats[stats['CID'].isin(player_list)]
    stats = stats.groupby(['CID']).sum()
    stats = calc_batting_stats(stats)
    stats = stats.drop(columns=['ORG', 'VLvl'])

    merged_df = pd.merge(cards, stats, on='CID')

    for col in merged_df.columns:
        merged_df[f'{col} Rk'] = merged_df[col].rank(
            ascending=False, method='max')

    first_pri = ['OBP', 'SBrate', 'RCrate']
    second_pri = ['RCrate', 'wOBA', 'OPS']
    third_pri = ['SLG', 'HRrate', 'OPS']
    fourth_pri = ['HRrate', 'SLG', 'OPS']
    fifth_pri = ['AVG', 'wOBA', 'OBP']
    sixth_pri = ['OBP', 'AVG', 'HRrate']
    seventh_pri = ['AVG', 'wOBA', 'OPS']
    eighth_pri = ['AVG', 'wOBA', 'OPS']
    ninth_pri = ['AVG', 'wOBA', 'OPS']

    merged_df['1'] = (merged_df[f'{first_pri[0]} Rk'] +
                      merged_df[f'{first_pri[1]} Rk'] +
                      merged_df[f'{first_pri[2]} Rk'])
    merged_df['2'] = (merged_df[f'{second_pri[0]} Rk'] +
                      merged_df[f'{second_pri[1]} Rk'] +
                      merged_df[f'{second_pri[2]} Rk'])
    merged_df['3'] = (merged_df[f'{third_pri[0]} Rk'] +
                      merged_df[f'{third_pri[1]} Rk'] +
                      merged_df[f'{third_pri[2]} Rk'])
    merged_df['4'] = (merged_df[f'{fourth_pri[0]} Rk'] +
                      merged_df[f'{fourth_pri[1]} Rk'] +
                      merged_df[f'{fourth_pri[2]} Rk'])
    merged_df['5'] = (merged_df[f'{fifth_pri[0]} Rk'] +
                      merged_df[f'{fifth_pri[1]} Rk'] +
                      merged_df[f'{fifth_pri[2]} Rk'])
    merged_df['6'] = (merged_df[f'{sixth_pri[0]} Rk'] +
                      merged_df[f'{sixth_pri[1]} Rk'] +
                      merged_df[f'{sixth_pri[2]} Rk'])
    merged_df['7'] = (merged_df[f'{seventh_pri[0]} Rk'] +
                      merged_df[f'{seventh_pri[1]} Rk'] +
                      merged_df[f'{seventh_pri[2]} Rk'])
    merged_df['8'] = (merged_df[f'{eighth_pri[0]} Rk'] +
                      merged_df[f'{eighth_pri[1]} Rk'] +
                      merged_df[f'{eighth_pri[2]} Rk'])
    merged_df['9'] = (merged_df[f'{ninth_pri[0]} Rk'] +
                      merged_df[f'{ninth_pri[1]} Rk'] +
                      merged_df[f'{ninth_pri[2]} Rk'])

    lineup_list = []

    for i in range(1, len(merged_df) + 1):
        df = merged_df.copy()
        fit = df.sort_values(by=f'{i}').loc[~df['CID'].isin(
            lineup_list)].iloc[0]
        lineup_list.append(fit['CID'])

    merged_df['CID'] = pd.Categorical(
        merged_df['CID'],
        categories=lineup_list,
        ordered=True
    )
    merged_df = merged_df.sort_values(by='CID').reset_index(drop=True)
    merged_df = merged_df[['Name', 'OBP', 'SLG', 'OPS', 'wOBA',
                           'RCrate', 'HRrate', 'SBrate']]
    return merged_df
