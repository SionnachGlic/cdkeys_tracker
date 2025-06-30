#cli.py
"""Command Line Interface for the CDKeys Price Tracker application."""

def cli_what_game() -> str:
    """Prompt the user for a game URL."""
    print("Please copy/paste the entire URL of the game you want to track:")
    url = input(str("URL: "))
    return url

def cli_show_game_details(title: str, current_price: float, unavailable: bool) -> None:
    """Show the user the game's details"""
    if unavailable:
        print(f"{title} is currently out of stock, but was £{current_price:.2f}.")
    else:
        print(f"The current price of {title} is £{current_price:.2f}")
    

def cli_what_price() -> float:
    """Prompt the user for a price threshold."""
    print("Please enter the maximum price you would pay for this game:")
    try:
        max_price = input("Maximum Price: £")
        max_price = float(max_price)
        return max_price
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return cli_what_price()  # Retry if input is invalid

def cli_check_update_duplicate(current_max_price: float) -> bool:
    """If a game is a duplicate, tell the user and give them the option to update its details
    If it's not a duplicate, do nothing."""

    print(f"This game is already in your list with a max price of £{current_max_price:.2f}.")
    print("Would you like to update its max price? (y/n)")
    user_input = ""
    while user_input != ('y' or 'n'):
        user_input = input(str())
        if user_input == 'y':
            print("Please enter the new max price you'd be willing to pay:")
            updated_price = input("Maximum Price: £")
            updated_price = float(updated_price)
            return True, updated_price
        elif user_input == 'n':
            print("Returning to previous menu.")
            return False, None
        else:
            print("Please enter a lowercase 'y' or 'n'.")
