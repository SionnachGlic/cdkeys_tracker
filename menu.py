from nicegui import ui

#Not working yet
def menu() -> None:
    """Create a menu with links to different pages."""
    ui.link('Home', '/')
    ui.link('Add Game', '/add_game')
    ui.link('View Games', '/view_games')
    ui.link('Remove Game', '/remove_game')
    ui.link('Update Game Price', '/update_game_price')
    ui.link('About', '/about')