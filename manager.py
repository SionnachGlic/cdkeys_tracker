#manager.py

"""Where the actual logic of the application is implemented:"""

from models.game import Game
from scraper.scraper import scrape_title, scrape_price, scrape_picture
from storage.csv_handler import save_to_csv, test_duplicate, csv_update_max_price, remove_from_csv
from cli.cli import cli_what_game, cli_what_price, cli_show_game_details, cli_check_update_duplicate 

class GameManager:
    @staticmethod
    def get_game_details(url: str) -> tuple[str, float, bool]:
        """Get game details from the URL."""
        title = scrape_title(url)
        current_price, unavailable = scrape_price(url)
        img_url = scrape_picture(url) #will probably have to add column for image URL in CSV file later
        return title, current_price, unavailable, img_url
    
    @staticmethod
    def check_duplicate(url: str) -> tuple[bool, float | None]:
        """Check if the game is already in the CSV file."""
        duplicate, current_max_price = test_duplicate(url)
        return duplicate, current_max_price
    
    #@staticmethod
    #def add_game(url: str, title: str, ):

    
    @staticmethod
    def remove_game(url: str):
        """Remove a game from the CSV file."""
        remove_from_csv(url)
