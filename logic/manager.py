#manager.py

"""Where the actual logic of the application is implemented:"""

from models.game import Game
from scraper.scraper import scrape_title, scrape_price
from storage.csv_handler import save_to_csv
from cli.cli import cli_what_game, cli_what_price

class GameManager:
    @staticmethod
    def add_game():
        url = cli_what_game()
        title = scrape_title(url)
        current_price = scrape_price(url)
        