from utils.modeling.fit_model import fit_model


def fit_batter_model(player_df):
    player_df = fit_model(
        player_df,
        'babip',
        'BABIP_pred',
        'bat'
    )
    player_df = fit_model(
        player_df,
        'strikeouts',
        'K_pred',
        'bat'
    )
    player_df = fit_model(
        player_df, 'walks', 'BB_pred', 'bat')
    player_df = fit_model(
        player_df,
        'homeruns',
        'HR_pred',
        'bat'
    )
    player_df = fit_model(
        player_df, 'xbh', 'XBH_pred', 'bat')
    player_df['K_pred'] = player_df['K_pred'].clip(lower=0)
    player_df['BB_pred'] = player_df['BB_pred'].clip(lower=0)
    player_df['HR_pred'] = player_df['HR_pred'].clip(lower=0)
    player_df['XBH_pred'] = player_df['XBH_pred'].clip(lower=0)

    player_df['K/600'] = round(player_df['K_pred'] * 600, 2)
    player_df['BB/600'] = round(player_df['BB_pred'] * 600, 2)
    player_df['tBIP'] = 600 - player_df['K/600'] - player_df['BB/600']
    player_df['HR/600'] = round(player_df['tBIP'] * player_df['HR_pred'], 2)
    player_df['nBIP'] = player_df['tBIP'] - player_df['HR/600']
    player_df['nHits'] = round(player_df['nBIP'] * player_df['BABIP_pred'], 1)
    player_df['XBH/600'] = player_df['nHits'] * player_df['XBH_pred']
    player_df['2B/600'] = round(player_df['XBH/600'] * .85, 2)
    player_df['3B/600'] = round(player_df['XBH/600'] * .15, 2)
    player_df['1B/600'] = round(player_df['nHits'] - player_df['XBH/600'], 2)
    player_df['AVG'] = round(
        (player_df['nHits'] + player_df['HR/600']) / (
                    600 - player_df['BB/600']),
        3)
    player_df['OBP'] = round(
        (player_df['nHits'] + player_df['HR/600'] + player_df[
            'BB/600'] + 4) / 600,
        3)
    player_df['SLG'] = round(
        (player_df['1B/600'] + (player_df['2B/600'] * 2) + (
                player_df['3B/600'] * 3) + (player_df['HR/600'] * 4)) / (
                600 - player_df['BB/600']), 3)
    player_df['OPS'] = round(player_df['OBP'] + player_df['SLG'], 3)
    player_df['wOBA'] = round(((player_df['BB/600'] * .701) + (4 * .722) + (
            player_df['1B/600'] * .895) + (player_df['2B/600'] * 1.270) + (
                                       player_df['3B/600'] * 1.608) + (
                                       player_df['HR/600'] * 2.072)) / (
                                      600 - 12), 3)

    return player_df
