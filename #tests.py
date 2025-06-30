#tests.py

from manager import GameManager
from storage.csv_handler import test_duplicate, csv_update_max_price

GameManager.cli_add_game()

#duplicate = test_duplicate('https://www.cdkeys.com/fortnite-transformers-pack-ps5-eu')
#print(f"Duplicate: {duplicate}")

#not_duplicate = test_duplicate('www.notduplicate.com')
#print(f"Not duplicate: {not_duplicate}")