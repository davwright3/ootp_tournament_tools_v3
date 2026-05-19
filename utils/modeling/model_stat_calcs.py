"""Utility for running calculations for models."""
import pandas as pd

def run_model_calcs(df, function_name):
    if function_name == 'babip':
        df = generate_babip_df(df)
    elif function_name == 'strikeouts':
        df = generate_strikeout_df(df)
    elif function_name == 'walks':
        df = generate_walk_df(df)
    elif function_name == 'homeruns':
        df = generate_hr_df(df)
    elif function_name == 'xbh':
        df = generate_xbh_df(df)
    elif function_name == 'p_strikeouts':
        df = generate_pit_strikeouts_df(df)
    elif function_name == 'p_walks':
        df = generate_pit_walks_df(df)
    elif function_name == 'p_homeruns':
        df = generate_pit_hr_df(df)
    elif function_name == 'p_babip':
        df = generate_pit_babip_df(df)



    return df


def generate_babip_df(df):
    df['BABIP Calc'] = round(
        (df['H'] - df['HR']) / (df['AB'] - df['K'] - df['HR'] + df['SF']), 4)

    return df

def generate_strikeout_df(df):
    df['Strikeout Calc'] = round(df['K'] / df['PA'], 4)
    return df

def generate_walk_df(df):
    df['Walk Calc'] = round(df['BB'] / df['PA'], 4)
    return df

def generate_hr_df(df):
    df['BIP'] = df['PA'] - df['K'] - df['BB'] - df['HP'] - df['IBB']
    df['HR Calc'] = round(df['HR'] / df['BIP'], 4)
    return df

def generate_xbh_df(df):
    df['XBH'] = df['2B'] + df['3B']
    df['XBH Calc'] = round(df['XBH'] / df['H'], 4)
    return df

def generate_pit_strikeouts_df(df):
    df['P_K_Calc'] = round(df['K_1'] / df['BF'], 4)
    return df

def generate_pit_walks_df(df):
    df['P_BB_Calc'] = round(df['BB_1'] / df['BF'], 4)
    return df

def generate_pit_hr_df(df):
    df['BIP'] = df['BF'] - df['K_1'] - df['BB_1'] - df['HP_1'] - df['IBB_1']
    df['P_HR_Calc'] = round(df['HR_1'] / df['BIP'], 4)
    return df

def generate_pit_babip_df(df):
    df['P_BABIP_Calc'] = round((df['HA'] - df['HR_1']) / (df['AB_1'] - df['K_1'] - df['HR_1'] + df['SF_1']), 4)
    return df