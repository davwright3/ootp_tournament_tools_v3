"""App for displaying player win rations in tournament environments."""
import tkinter as tk
from utils.view_utils.header_frame import Header
from utils.view_utils.footer_frame import Footer
from utils.view_utils.dataframe_table_frame import DataFrameTableFrame
from utils.stats_utils.calc_player_win_ratios import calc_player_win_ratios
from utils.view_utils.min_max_rating_frame import MinMaxFrame
from utils.view_utils.position_select_frame import PositionSelectFrame
from utils.view_utils.minimum_trny_app_frame import MinTrnyAppFrame


class PlayerWinRatios(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Player Win Ratios")
        self.geometry('1920x1080')

        self.number_of_teams = tk.StringVar(value='16')
        self.games_per_round = tk.StringVar(value='5')
        self.games_per_finals = tk.StringVar(value='5')

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

        self.header_frame = Header(self, app_name='Player Win Ratios')
        self.header_frame.grid(row=0, column=0, sticky='nsew')

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, sticky='nsew')

        self.footer_frame = Footer(self)
        self.footer_frame.grid(row=2, column=0, sticky='nsew')

        # Main Frame setup
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=1)

        self.results_view_frame = DataFrameTableFrame(self.main_frame)
        self.results_view_frame.grid(row=0, column=0, sticky='nsew')

        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.grid(row=0, column=1, sticky='nsew')

        self.options_frame.columnconfigure(0, weight=1)
        self.options_frame.columnconfigure(1, weight=1)

        row = 0
        self.options_label = tk.Label(self.options_frame, text='Options Frame')
        self.options_label.grid(row=row, column=0, sticky='nsew', columnspan=2)
        row += 1

        # Set up the options frame
        # TODO Number of teams
        # TODO numbers of games per round
        # TODO number of games in finals
        # TODO Button to run the data
        # TODO Position/ratings/etc selection
        self.run_player_win_ratios_button = tk.Button(self.options_frame, text='Run Calcs', command=self.run_player_win_ratios)
        self.run_player_win_ratios_button.grid(row=row, column=0, sticky='nsew', columnspan=2, padx=3, pady=3)
        row += 1

        self.num_of_teams_label = tk.Label(self.options_frame, text='Teams: ')
        self.num_of_teams_label.grid(row=row, column=0, sticky='nsew', padx=3, pady=3)

        self.num_of_teams_entry = tk.Entry(self.options_frame, textvariable=self.number_of_teams)
        self.num_of_teams_entry.grid(row=row, column=1, sticky='nsew', padx=3, pady=3)
        row += 1

        self.games_per_round_label = tk.Label(self.options_frame, text='Best Of: ')
        self.games_per_round_label.grid(row=row, column=0, sticky='nsew', padx=3, pady=3)

        self.games_per_round_entry = tk.Entry(self.options_frame, textvariable=self.games_per_round)
        self.games_per_round_entry.grid(row=row, column=1, sticky='nsew', padx=3, pady=3)
        row += 1

        self.games_per_finals_label = tk.Label(self.options_frame, text='Finals BO: ')
        self.games_per_finals_label.grid(row=row, column=0, sticky='nsew', padx=3, pady=3)

        self.games_per_finals_entry = tk.Entry(self.options_frame, textvariable=self.games_per_finals)
        self.games_per_finals_entry.grid(row=row, column=1, sticky='nsew', padx=3, pady=3)
        row += 1

        self.min_apps_frame = MinTrnyAppFrame(self.options_frame)
        self.min_apps_frame.grid(row=row, column=0, sticky='nsew', columnspan=2)
        row += 1

        self.min_max_rating_frame = MinMaxFrame(self.options_frame)
        self.min_max_rating_frame.grid(row=row, column=0, sticky='nsew', columnspan=2, padx=3, pady=3)
        row += 1

        self.position_select_frame = PositionSelectFrame(self.options_frame)
        self.position_select_frame.grid(row=row, column=0, sticky='nsew', padx=3, pady=3, columnspan=2)
        row += 1



    def run_player_win_ratios(self):
        print('Running Player Win Ratios')
        try:
            set_num_teams = int(self.number_of_teams.get())
            set_games_per_round = int(self.games_per_round.get())
            set_games_per_finals = int(self.games_per_finals.get())
            min_rating, max_rating = self.min_max_rating_frame.get_min_max_rating()
            set_min_rating = int(min_rating)
            set_max_rating = int(max_rating)
        except ValueError:
            set_num_teams = 16
            set_games_per_round = 5
            set_games_per_finals = 5
            set_min_rating, set_max_rating = 40, 105

        selected_position = self.position_select_frame.get_position_select()
        selected_min_apps = self.min_apps_frame.get_min_apps()


        ratios_df = calc_player_win_ratios(
            set_num_teams,
            set_games_per_round,
            set_games_per_finals,
            min_apps=selected_min_apps,
            min_rating=set_min_rating,
            max_rating=set_max_rating,
            position_select=selected_position,

        )
        self.results_view_frame.set_dataframe(ratios_df)



