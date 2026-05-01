"""
App module for displaying ratios of left and right-handed batters
and pitchers
"""
import tkinter as tk
from tkinter import ttk
from utils.data_utils.data_store import data_store
from utils.data_utils.card_list_store import card_list_store
from utils.stats_utils.normalize_innings_pitched import normalize_innings_pitched
import pandas as pd


class DisplayTourneySplits(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Tournament Ratios")
        self.geometry("600x800")

        set_font = ('Arial', 20, 'bold')

        data = data_store.get_data().copy()[['CID', 'PA', 'IP']]
        data['IPC'] = data['IP'].apply(normalize_innings_pitched)
        cards = card_list_store.get_card_list().copy()[['Card ID', 'Bats', 'Throws']]
        cards = cards.rename(columns={'Card ID': 'CID'})

        df = pd.merge(cards, data, how='inner', on='CID')
        df = df.drop(columns=['CID'])
        bats = df[['Bats', 'PA']].groupby(by='Bats', as_index=False).sum()
        throws = df[['Throws', 'IPC']].groupby(by='Throws', as_index=False).sum()

        total_pa = bats['PA'].sum()
        left_pa = bats[bats['Bats'] == 1]['PA'].sum()
        left_pa_pct = round((int(left_pa) / total_pa) * 100, 1)
        right_pa = bats[bats['Bats'] == 2]['PA'].sum()
        right_pa_pct = round((int(right_pa) / total_pa) * 100, 1)
        switch_pa = bats[bats['Bats'] == 3]['PA'].sum()
        switch_pa_pct = round((int(switch_pa) / total_pa) * 100, 1)

        total_ip = throws['IPC'].sum()
        left_ip = throws[throws['Throws'] == 2]['IPC'].sum()
        left_ip_pct = round((int(left_ip) / total_ip) * 100, 1)
        right_ip = throws[throws['Throws'] == 1]['IPC'].sum()
        right_ip_pct = round((int(right_ip) / total_ip) * 100, 1)

        self.total_pa_label = tk.Label(
            self,
            text=f'Total PA: {total_pa}',
            font=set_font
        )
        self.total_pa_label.grid(row=0, column=0, padx=10, pady=10)

        self.left_pa_label = tk.Label(
            self,
            text=f'Left PA: {left_pa} ({left_pa_pct}%)',
            font=set_font
        )
        self.left_pa_label.grid(row=1, column=0, padx=10, pady=10)

        self.right_pa_label = tk.Label(
            self,
            text=f'Right PA: {right_pa} ({right_pa_pct}%)',
            font=set_font
        )
        self.right_pa_label.grid(row=2, column=0, padx=10, pady=10)

        self.switch_pa_label = tk.Label(
            self,
            text=f'Switch PA: {switch_pa} ({switch_pa_pct}%)',
            font=set_font
        )
        self.switch_pa_label.grid(row=3, column=0, padx=10, pady=10)

        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=4, column=0, padx=10, pady=10)

        self.total_ip_label = tk.Label(
            self,
            text=f'Total IP: {total_ip}',
            font=set_font
        )
        self.total_ip_label.grid(row=5, column=0, padx=10, pady=10)

        self.left_ip_label = tk.Label(
            self,
            text=f'Left IP: {round(left_ip, 2)} ({left_ip_pct}%)',
            font=set_font
        )
        self.left_ip_label.grid(row=6, column=0, padx=10, pady=10)

        self.right_ip_label = tk.Label(
            self,
            text=f'Right IP: {round(right_ip, 2)} ({right_ip_pct}%)',
            font=set_font
        )
        self.right_ip_label.grid(row=7, column=0, padx=10, pady=10)


