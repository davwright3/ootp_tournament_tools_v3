import pandas as pd
from utils.stats_utils.calc_batting_stats import calc_batting_stats
from utils.stats_utils.calc_pitching_stats import calculate_pitching_stats
from utils.data_utils.data_store import data_store
from utils.data_utils.card_list_store import card_list_store
from utils.stats_utils.cull_teams import cull_teams
from utils.stats_utils.normalize_innings_pitched import (
    normalize_innings_pitched)


def generate_player_stats_for_team_df(team_name=None):
    if team_name is None:
        return

    df1 = cull_teams(data_store.get_data().copy())
    df1 = df1[df1['ORG'] == team_name]
    df1['IPC'] = df1['IP'].apply(normalize_innings_pitched)
    df2 = df1.copy()

    card_list = card_list_store.get_card_list().copy()
    card_list = card_list.rename(
        columns={'Card ID': 'CID', '//Card Title': 'Title'})
    card_list_2 = card_list.copy()

    df1 = df1[['CID', 'VLvl', 'PA', 'AB', 'H', '1B', '2B', '3B',
               'HR', 'TB', 'K', 'HP', 'BB', 'IBB', 'SF', 'SB',
               'CS', 'WAR', 'RC', 'TC', 'A', 'PO', 'E', 'ZR',
               'SBA', 'RTO']].groupby(['CID', 'VLvl'], as_index=False).sum()

    df2 = df2[['CID', 'VLvl', 'IPC', 'G_1', 'GS_1', 'BF', 'AB_1', 'ER', 'K_1',
               'BB_1', 'IBB_1', 'HA', '1B_1', '2B_1', '3B_1', 'HR_1', 'SV',
               'SVO', 'SD', 'MD', 'HP_1', 'SH_1', 'SF_1', 'QS', 'IR', 'IRS',
               'GB', 'FB', 'WAR_1', 'Trny']].groupby(['CID', 'VLvl'],
                                                     as_index=False).sum()
    df1 = df1[df1['PA'] > 0]
    df2 = df2[df2['IPC'] > 0]

    batters = calc_batting_stats(df1, min_pa=20)
    pitchers = calculate_pitching_stats(df2, min_ip_sel=20)

    batters = batters[['CID', 'VLvl', 'PA', 'WARrate']]
    pitchers = pitchers[['CID', 'VLvl', 'IPC', 'ERA']]

    batters_full = pd.merge(
        card_list[['CID', 'Title']],
        batters,
        how='inner',
        on='CID')
    batters_full = batters_full.sort_values(by='PA', ascending=False)
    pitchers_full = pd.merge(
        card_list_2[['CID', 'Title']],
        pitchers,
        how='inner',
        on='CID')
    pitchers_full = pitchers_full.sort_values(by='IPC', ascending=False)

    return batters_full, pitchers_full
