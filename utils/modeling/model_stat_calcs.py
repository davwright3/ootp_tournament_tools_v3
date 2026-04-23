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