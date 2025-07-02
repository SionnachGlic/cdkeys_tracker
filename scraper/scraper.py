#game_scraper.py

import requests
from bs4 import BeautifulSoup as BS

"""Contains the functions to scrape the title, price, and availability of a game from cdkeys.com"""

def scrape_title(url):
    """Get the title from the web page"""

    #try/except commented out til I sort how to display errors that work for cli and gui
    page = requests.get(url, timeout=10)

    soup = BS(page.content, 'html.parser')

    #Get title of product (previously page)
    title = soup.find(class_="product-title").get_text()

    #try:
        #page = requests.get(url, timeout=10)

        #soup = BS(page.content, 'html.parser')

        #Get title of product (previously page)
        #title = soup.find(class_="product-title").get_text()
    
    #a bunch of this is commented out because it doesn't work for some reason
    #and I don't know why, so I will leave it for now
    #except requests.exceptions.ConnectionError as conn_err:
        #print("Connection error, please check your internet connection or cdkeys.com status.")
        #print(f"scrape_title ConnectionError: {conn_err}")
        #go back to add game menu
        #Game.add_game()

    #except requests.exceptions.Timeout as timeout_err:
        #print("Request timed out, please check your connection and the status of cdkeys.com.")
        #print(f"scrape_title TimeoutError: {timeout_err}")
        #go back to add game menu
        #Game.add_game()
    
    #except AttributeError:
        #print("scrape_title AttributeError: Please check URL is correct.")
        #print("If problem continues, the web page structure may have changed, please report this issue.")
        #go back to add game menu
        #Game.add_game()
        #return None
    
    #except requests.exceptions.RequestException as req_err:
        #print("An error occurred while trying to fetch the page, please check your connection and the status of cdkeys.com")
        #print(f"scrape_title RequestException: {req_err}")
        #go back to add game menu
        #Game.add_game()
    
    #except Exception as e:
        #print(f"An unexpected error occurred, please check your connection and the status of cdkeys.com")
        #print("If error persists, please report it.")
        #print(f"error: {e}")
        #go back to add game menu
        #Game.add_game()
        #return None

    #strip whitespace from start and end of title
    title = title.strip()
        
    return title

def scrape_price(url):
    """Get the price from the web page"""

    def price_to_float(price_str):
        """Convert price from string with currency sign to float"""
        
        #start with empty string
        current_price = ""
        
        #first get string of just the value
        for char in price_str:
            if char.isdigit() or char == '.':
                current_price += char
        
        #convert to float
        current_price = float(current_price)
        return current_price
    
    def is_unavailable(url):
        try:
            page = requests.get(url)
            soup = BS(page.content, 'html.parser')

            div = soup.find(class_='product-info-main')
            unavailable = div.find('span', id='notify-me')
            if unavailable:
                return True
            else:
                return False
        except (AttributeError, IndexError):
            return False

    #try/except blocks commented out til I figure out how to raise errors for cli and gui
    page = requests.get(url)

    soup = BS(page.content, 'html.parser')

    #Check if available
    unavailable = is_unavailable(url)

    try:
        #try to find price after discounts
        price_str = soup.find(class_="final-price").get_text()
    
    except AttributeError:

        #get original price if no discounted price found
        price_str = soup.find(class_="price").get_text()
    
    #try:
        #page = requests.get(url)

        #soup = BS(page.content, 'html.parser')

        #Check if available
        #unavailable = is_unavailable(url)

        #try:
            #try to find price after discounts
            #price_str = soup.find(class_="final-price").get_text()
        
        #except AttributeError:

            #get original price if no discounted price found
            #price_str = soup.find(class_="price").get_text()

            #try/except blocks commented out til I figure out how to handle errors that works for gui and cli
            #try:
                #get original price if no discounted price found
                #price_str = soup.find(class_="price").get_text()

            #except AttributeError:
                    #print("scrape_price AttributeError: Web page structure may have changed, please report this issue.")
                    #return None, None
        
    #except AttributeError:
        #print("scrape_price AttributeError: Web page structure may have changed, please report this issue.")
        #return None, None
    
    #except Exception as e:
        #print(f"An unexpected error occurred, please check your connection and the status of cdkeys.com")
        #print("If error persists, please report it.")
        #print(f"error: {e}")
        #go back to add game menu
        #Game.add_game() 
        #return None, None


    current_price = price_to_float(price_str)
    return current_price, unavailable