"""Frame for filling custom player data to return model."""
import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils.modeling.fit_batters_model import fit_batters_model


class CustomPlayerModelFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', bd=3)

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)


        # Variables for entries
        self.avoidk_ovr_var = tk.StringVar(value='40')
        self.avoidk_vl_var = tk.StringVar(value='40')
        self.avoidk_vr_var = tk.StringVar(value='40')
        self.babip_ovr_var = tk.StringVar(value='40')
        self.babip_vl_var = tk.StringVar(value='40')
        self.babip_vr_var = tk.StringVar(value='40')
        self.gap_ovr_var = tk.StringVar(value='40')
        self.gap_vl_var = tk.StringVar(value='40')
        self.gap_vr_var = tk.StringVar(value='40')
        self.power_ovr_var = tk.StringVar(value='40')
        self.power_vl_var = tk.StringVar(value='40')
        self.power_vr_var = tk.StringVar(value='40')
        self.eye_ovr_var = tk.StringVar(value='40')
        self.eye_vl_var = tk.StringVar(value='40')
        self.eye_vr_var = tk.StringVar(value='40')
        self.baserunning_var = tk.StringVar(value='40')
        self.speed_var = tk.StringVar(value='40')
        self.battedballtype_var = tk.StringVar(value='0')
        self.bats_var = tk.StringVar(value='1')

        self.average_display_var = tk.StringVar(value='AVG: .000')
        self.obp_display_var = tk.StringVar(value='OBP: .000')
        self.slg_display_var = tk.StringVar(value='SLG: .000')
        self.ops_display_var = tk.StringVar(value='OPS: .000')
        self.woba_display_var = tk.StringVar(value='WOBA: .000')
        self.homerun_display_var = tk.StringVar(value='HR/600: .000')


        self.label = tk.Label(self, text="Custom Player Model")
        self.label.grid(row=0, column=0, sticky='nsew')

        self.avoidk_label = tk.Label(self, text="Avoidk")
        self.avoidk_label.grid(row=2, column=0, sticky='nsew')
        self.babip_label = tk.Label(self, text="BABIP")
        self.babip_label.grid(row=3, column=0, sticky='nsew')
        self.gap_label = tk.Label(self, text="GAP")
        self.gap_label.grid(row=4, column=0, sticky='nsew')
        self.power_label = tk.Label(self, text="Power")
        self.power_label.grid(row=5, column=0, sticky='nsew')
        self.eye_label = tk.Label(self, text="Eye")
        self.eye_label.grid(row=6, column=0, sticky='nsew')

        self.overall_label = tk.Label(self, text="OVR")
        self.overall_label.grid(row=1, column=1, sticky='nsew')
        self.vs_left_label = tk.Label(self, text="vL")
        self.vs_left_label.grid(row=1, column=2, sticky='nsew')
        self.vs_right_label = tk.Label(self, text="vR")
        self.vs_right_label.grid(row=1, column=3, sticky='nsew')

        self.avoidk_ovr_entry = tk.Entry(self, textvariable=self.avoidk_ovr_var)
        self.avoidk_ovr_entry.grid(row=2, column=1, sticky='nsew')
        self.avoidk_vl_entry = tk.Entry(self, textvariable=self.avoidk_vl_var)
        self.avoidk_vl_entry.grid(row=2, column=2, sticky='nsew')
        self.avoidk_vr_entry = tk.Entry(self, textvariable=self.avoidk_vr_var)
        self.avoidk_vr_entry.grid(row=2, column=3, sticky='nsew')

        self.babip_ovr_entry = tk.Entry(self, textvariable=self.babip_ovr_var)
        self.babip_ovr_entry.grid(row=3, column=1, sticky='nsew')
        self.babip_vl_entry = tk.Entry(self, textvariable=self.babip_vl_var)
        self.babip_vl_entry.grid(row=3, column=2, sticky='nsew')
        self.babip_vr_entry = tk.Entry(self, textvariable=self.babip_vr_var)
        self.babip_vr_entry.grid(row=3, column=3, sticky='nsew')

        self.gap_ovr_entry = tk.Entry(self, textvariable=self.gap_ovr_var)
        self.gap_ovr_entry.grid(row=4, column=1, sticky='nsew')
        self.gap_vl_entry = tk.Entry(self, textvariable=self.gap_vl_var)
        self.gap_vl_entry.grid(row=4, column=2, sticky='nsew')
        self.gap_vr_entry = tk.Entry(self, textvariable=self.gap_vr_var)
        self.gap_vr_entry.grid(row=4, column=3, sticky='nsew')

        self.power_ovr_entry = tk.Entry(self, textvariable=self.power_ovr_var)
        self.power_ovr_entry.grid(row=5, column=1, sticky='nsew')
        self.power_vl_entry = tk.Entry(self, textvariable=self.power_vl_var)
        self.power_vl_entry.grid(row=5, column=2, sticky='nsew')
        self.power_vr_entry = tk.Entry(self, textvariable=self.power_vr_var)
        self.power_vr_entry.grid(row=5, column=3, sticky='nsew')

        self.eye_ovr_entry = tk.Entry(self, textvariable=self.eye_ovr_var)
        self.eye_ovr_entry.grid(row=6, column=1, sticky='nsew')
        self.eye_vl_entry = tk.Entry(self, textvariable=self.eye_vl_var)
        self.eye_vl_entry.grid(row=6, column=2, sticky='nsew')
        self.eye_vr_entry = tk.Entry(self, textvariable=self.eye_vr_var)
        self.eye_vr_entry.grid(row=6, column=3, sticky='nsew')

        self.separator_one = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator_one.grid(row=7, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

        self.speed_label = tk.Label(self, text="Speed")
        self.speed_label.grid(row=8, column=0, sticky='nsew')
        self.baserunning_label = tk.Label(self, text="Baserunning")
        self.baserunning_label.grid(row=9, column=0, sticky='nsew')
        self.batted_ball_type_label = tk.Label(self, text="BBT (N: 0, GB: 1, FB:2, LD:3)")
        self.batted_ball_type_label.grid(row=10, column=2, sticky='nsew')
        self.bats_label = tk.Label(self, text="Bats (L:1, R:2, S: 3)")
        self.bats_label.grid(row=8, column=2, sticky='nsew')

        self.speed_entry = tk.Entry(self, textvariable=self.speed_var)
        self.speed_entry.grid(row=8, column=1, sticky='nsew')
        self.baserunning_entry = tk.Entry(self, textvariable=self.baserunning_var)
        self.baserunning_entry.grid(row=9, column=1, sticky='nsew')
        self.batted_ball_type_entry = tk.Entry(self, textvariable=self.battedballtype_var)
        self.batted_ball_type_entry.grid(row=10, column=3, sticky='nsew')
        self.bats_entry = tk.Entry(self, textvariable=self.bats_var)
        self.bats_entry.grid(row=8, column=3, sticky='nsew')

        self.run_custom_model_button = tk.Button(self, text='Run Model', command=self.run_custom_model)
        self.run_custom_model_button.grid(row=10, column=0, sticky='nsew')

        self.separator_two = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator_two.grid(row=11, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

        self.average_display = tk.Label(self, textvariable=self.average_display_var)
        self.average_display.grid(row=12, column=0, sticky='nsew', columnspan=2)

        self.obp_display = tk.Label(self, textvariable=self.obp_display_var)
        self.obp_display.grid(row=12, column=2, sticky='nsew', columnspan=2)

        self.slg_display = tk.Label(self, textvariable=self.slg_display_var)
        self.slg_display.grid(row=13, column=0, sticky='nsew', columnspan=2)

        self.ops_display = tk.Label(self, textvariable=self.ops_display_var)
        self.ops_display.grid(row=13, column=2, sticky='nsew', columnspan=2)

        self.woba_display = tk.Label(self, textvariable=self.woba_display_var)
        self.woba_display.grid(row=14, column=0, sticky='nsew', columnspan=2)

        self.homerun_display = tk.Label(self, textvariable=self.homerun_display_var)
        self.homerun_display.grid(row=14, column=2, sticky='nsew', columnspan=2)

    def run_custom_model(self):
        print('Running custom model')
        try:
            player_df = pd.DataFrame()
            player_df.loc[0, '//Card Title'] = 'Custom Player'
            player_df.loc[0, 'Card Value'] = 80
            player_df.loc[0, 'Year'] = 1960
            player_df.loc[0, 'Avoid Ks'] = int(self.avoidk_ovr_var.get())
            player_df.loc[0, 'Avoid K vL'] = int(self.avoidk_vl_var.get())
            player_df.loc[0, 'Avoid K vR'] = int(self.avoidk_vr_var.get())
            player_df.loc[0, 'BABIP'] = int(self.babip_ovr_var.get())
            player_df.loc[0, 'BABIP vL'] = int(self.babip_vl_var.get())
            player_df.loc[0, 'BABIP vR'] = int(self.babip_vr_var.get())
            player_df.loc[0, 'Gap'] = int(self.gap_ovr_var.get())
            player_df.loc[0, 'Gap vL'] = int(self.gap_vl_var.get())
            player_df.loc[0, 'Gap vR'] = int(self.gap_vr_var.get())
            player_df.loc[0, 'Power'] = int(self.power_ovr_var.get())
            player_df.loc[0, 'Power vL'] = int(self.power_vl_var.get())
            player_df.loc[0, 'Power vR'] = int(self.power_vr_var.get())
            player_df.loc[0, 'Eye'] = int(self.eye_ovr_var.get())
            player_df.loc[0, 'Eye vL'] = int(self.eye_vl_var.get())
            player_df.loc[0, 'Eye vR'] = int(self.eye_vr_var.get())
            player_df.loc[0, 'Bats'] = int(self.bats_var.get())
            player_df.loc[0, 'Speed'] = int(self.speed_var.get())
            player_df.loc[0, 'Baserunning'] = int(self.baserunning_var.get())
            player_df.loc[0, 'BattedBallType'] = int(self.battedballtype_var.get())
            player_df['Bats'] = player_df['Bats'].astype(int)
            player_df['BattedBallType'] = player_df['BattedBallType'].astype(int)

            player_df = fit_batters_model(player_df, 'babip', 'BABIP_pred', ['BABIP', 'BABIP vL', 'BABIP vR', 'Speed'])
            player_df = fit_batters_model(player_df, 'strikeouts', 'K_pred', ['Avoid Ks', 'Avoid K vL', 'Avoid K vR'])
            player_df = fit_batters_model(player_df, 'walks', 'BB_pred', ['Eye', 'Eye vL', 'Eye vR'])
            player_df = fit_batters_model(player_df, 'homeruns', 'HR_pred', ['Power', 'Power vL', 'Power vR'])
            player_df = fit_batters_model(player_df, 'xbh', 'XBH_pred', ['Gap', 'Gap vL', 'Gap vR', 'Baserunning', 'Speed'])
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
                (player_df['nHits'] + player_df['HR/600']) / (600 - player_df['BB/600']),
                3)
            player_df['OBP'] = round(
                (player_df['nHits'] + player_df['HR/600'] + player_df['BB/600'] + 4) / 600,
                3)
            player_df['SLG'] = round((player_df['1B/600'] + (player_df['2B/600'] * 2) + (
                        player_df['3B/600'] * 3) + (player_df['HR/600'] * 4)) / (
                                             600 - player_df['BB/600']), 3)
            player_df['OPS'] = round(player_df['OBP'] + player_df['SLG'], 3)
            player_df['wOBA'] = round(((player_df['BB/600'] * .701) + (4 * .722) + (
                        player_df['1B/600'] * .895) + (player_df['2B/600'] * 1.270) + (
                                               player_df['3B/600'] * 1.608) + (
                                               player_df['HR/600'] * 2.072)) / (
                                              600 - 12), 3)

            return_df = player_df[['AVG', 'OBP', 'SLG', 'OPS', 'wOBA', 'HR/600']]

            self.average_display_var.set(f'AVG: {return_df.loc[0]['AVG']}')
            self.obp_display_var.set(f'OBP: {return_df.loc[0]['OBP']}')
            self.slg_display_var.set(f'SLG: {return_df.loc[0]['SLG']}')
            self.ops_display_var.set(f'OPS: {return_df.loc[0]['OPS']}')
            self.woba_display_var.set(f'WOBA: {return_df.loc[0]['wOBA']}')
            self.homerun_display_var.set(f'HR/600: {return_df.loc[0]['HR/600']}')
            




        except Exception as e:
            print(e)
            return

        print(return_df)

