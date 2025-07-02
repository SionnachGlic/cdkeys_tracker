#manager.py

"""Where the actual logic of the application is implemented:"""

from models.game import Game
from scraper.scraper import scrape_title, scrape_price
from storage.csv_handler import save_to_csv, test_duplicate, csv_update_max_price, remove_from_csv
from cli.cli import cli_what_game, cli_what_price, cli_show_game_details, cli_check_update_duplicate 

class GameManager:
    @staticmethod
    def cli_add_game():
        """Add a game to the list by scraping its details from the provided URL and getting user's price threshold.
        If the game is already in the list, prompt the user to update its max price."""
        url = cli_what_game()
        title = scrape_title(url)
        current_price, unavailable = scrape_price(url)
        is_duplicate, current_max_price = test_duplicate(url)
        cli_show_game_details(title, current_price, unavailable)
        if is_duplicate:
            update_duplicate, updated_price = cli_check_update_duplicate(current_max_price)
            if update_duplicate:
                csv_update_max_price(url, updated_price)
            else:
                GameManager.cli_add_game()
        else:        
            max_price = cli_what_price()
            game_instance = Game(url, title, current_price, max_price)
            save_to_csv(game_instance, "game_price_list.csv")
    
    @staticmethod
    def cli_remove_game():
        """Remove a game from the list by its URL."""
        url = cli_what_game()
        remove_from_csv(url)
