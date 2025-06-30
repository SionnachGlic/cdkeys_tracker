#cli.py
"""Command Line Interface for the CDKeys Price Tracker application."""

def cli_what_game() -> str:
    """Prompt the user for a game URL."""
    print("Please copy/paste the entire URL of the game you want to track:")
    url = input(str("URL: "))
    return url

def cli_show_game_details(title: str, current_price: float) -> None:
    pass

def cli_what_price() -> float:
    """Prompt the user for a price threshold."""
    print("Please enter the maximum price you would pay for this game:")
    try:
        max_price = input(float("Maximum Price: £"))
        return max_price
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return cli_what_price()  # Retry if input is invalid