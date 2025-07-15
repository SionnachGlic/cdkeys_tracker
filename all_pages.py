from nicegui import ui
from pages.add_game_page import add_game_page
from pages.view_games_page import view_games_page
from pages.remove_game_page import remove_game_page
from pages.update_game_price_page import update_game_price_page
from pages.about_page import about_page


def create() -> None:
    ui.page('/add_game'),(add_game_page)
    ui.page('/view_games')(view_games_page)
    ui.page('/remove_game')(remove_game_page)
    ui.page('/update_game_price')(update_game_price_page)
    ui.page('/about')(about_page)

if __name__ == '__main__':
    create()