#cdkeys_price_get_input

"""Allows user to enter a url of a desired game on cdkeys.com, and tells them the title and
current price. Then asks them the maximum price they're willing to pay and saves these details in a csv."""

#requests data from web pages
import requests

#searches for specific things
from bs4 import BeautifulSoup as BS

#for file management eg checking if csv file already exists
import os

#to save in spreadsheet
import csv


class Game:
    
    def __init__(self, url, title, price_float = None, max_price = None):
        """set instance variables to values"""
        self.url = url
        self.title = title
        self.price_float = price_float
        self.max_price = max_price

    def save_to_csv(self, filename = "game_price_list.csv"):

        #check if file exists already
        file_exists = os.path.exists(filename)

        #open the csv file in append mode, create a new line, and use character
        #encoding in case the title has special chatacters
        with open(filename, mode = 'a', newline = '', encoding = 'utf-8') as file:
            
            #create csv writer object
            writer = csv.writer(file)

            #if file doesn't exist then make one with the headers
            if not file_exists:
                writer.writerow(['url', 'title', 'current_price', 'max_price'])
            
            #write attributes of current game instance in different columns
            writer.writerow([self.url, self.title, self.price_float, self.max_price])
        
    @staticmethod
    def scrape_title(url):
        """Get the title from the web page"""

        try:
            page = requests.get(url, timeout=10)

            soup = BS(page.content, 'html.parser')

            #Get title of product (previously page)
            title = soup.find(class_="product-title").get_text()
        
        #a bunch of this is commented out because it doesn't work for some reason
        #and I don't know why, so I will leave it for now

        #except requests.exceptions.ConnectionError as conn_err:
            #print("Connection error, please check your internet connection or cdkeys.com status.")
            #print(f"scrape_title ConnectionError: {conn_err}")
            #go back to add game menu
            #Game.add_game(Game)

        #except requests.exceptions.Timeout as timeout_err:
            #print("Request timed out, please check your connection and the status of cdkeys.com.")
            #print(f"scrape_title TimeoutError: {timeout_err}")
            #go back to add game menu
            #Game.add_game(Game)
        
        except AttributeError:
            print("scrape_title AttributeError: Please check URL is correct.")
            print("If problem continues, the web page structure may have changed, please report this issue.")
            #go back to add game menu
            Game.add_game(Game)
        
        #except requests.exceptions.RequestException as req_err:
            #print("An error occurred while trying to fetch the page, please check your connection and the status of cdkeys.com")
            #print(f"scrape_title RequestException: {req_err}")
            #go back to add game menu
            #Game.add_game(Game)
        
        except Exception as e:
            print(f"An unexpected error occurred, please check your connection and the status of cdkeys.com")
            print("If error persists, please report it.")
            print(f"error: {e}")
            #go back to add game menu
            Game.add_game(Game)

        #strip whitespace from start and end of title
        title = title.strip()
            
        return title

    @staticmethod
    def scrape_price(url):
        """Get the price from the web page"""

        def price_to_float(price_str):
            """Convert price from string with currency sign to float"""
            
            #if game is out of stock, price is infinite, so always more than max price
            if not price_str:
                 price_float = float('inf')
            
            else:
                #start with empty string
                price_float = ""
                
                #first get string of just the value
                for char in price_str:
                    if char.isdigit() or char == '.':
                        price_float += char
                
                #convert to float
                price_float = float(price_float)
                return price_float
        
        try:
            page = requests.get(url)

            soup = BS(page.content, 'html.parser')

            #Check if available
            unavailable = soup.find(class_="unavailable")
            if unavailable:
                #if unavailable, set price to a high value so it is always more than max price
                #and can be used to alert user that the game is out of stock
                #there should be a better way of doing this using inf?
                price_str = "999999"
        
            else:

                try:
                    #try to find price after discounts
                    price_str = soup.find(class_="final-price").get_text()
                
                except AttributeError:
                    try:
                        #get original price if no discounted price found
                        price_str = soup.find(class_="price").get_text()

                    except AttributeError:
                            print("scrape_price AttributeError: Web page structure may have changed, please report this issue.")
            
        except AttributeError:
            print("scrape_price AttributeError: Web page structure may have changed, please report this issue.")
        
        except Exception as e:
            print(f"An unexpected error occurred, please check your connection and the status of cdkeys.com")
            print("If error persists, please report it.")
            print(f"error: {e}")
            #go back to add game menu
            Game.add_game(Game) 


        price_float = price_to_float(price_str)
        return price_float
        
    def add_game(cls):
        """allows the user to input the game's url and their max price"""
        
        print("Enter 'q' to quit at any time and return to the previous menu")
        user_input = ""
        
        while True:

            print()
            print("What is the URL of the product you want to track?")
            user_input = input(str())
            
            #if user quits return to add or remove game menu
            if user_input == 'q':
                Game.add_or_remove(Game)

            
            #Scrape the title and price from the given url
            url = user_input
            title = cls.scrape_title(url)
            price_float = cls.scrape_price(url)

            print()
            if price_float == float(999999):
                print(f"{title} is currently out of stock.")
            else:
                print(f"The current price of {title} is £{price_float:.2f}.")
            
            print()
            print("What is the maximum price you're willing to pay for this?")
            user_input = input("£")
            
            if user_input == 'q': #There must be a neater way of doing this without repeating it?
                Game.add_or_remove(Game)
            
            max_price = float(user_input)

            #add this game's details to csv
            game_instance = cls(url, title, price_float, max_price)
            game_instance.save_to_csv()
            print()
            print("Game information saved")

    def remove_game(cls, filename = "game_price_list.csv"):
        """Allows the user to enter the url of the game they'd like to remove"""

        print("Enter 'q' to quit at any time")
        user_input = ""

        while True:

            print()
            print("What is the URL of the product you'd like to remove?")
            user_input = input(str())
            
            #stop if user quits
            if user_input == 'q':
                Game.add_or_remove(Game)

            #Initialise rows_to_keep as empty list
            rows_to_keep = []

            #Initialise removed_game as None
            removed_game = None

            #read csv to find row that has url
            with open(filename, mode = 'r', newline = '', encoding = 'utf-8') as file:
                
                reader = csv.reader(file)
                
                #extracts first row and stores it in variable called header
                header = next(reader)

                #creates index so removed game is recorded to inform user
                url_index = header.index('url')
                title_index = header.index('title')
                
                for row in reader:
                    
                    if row[url_index] == user_input:
                        removed_game = row #Store removed game
                        
                    else:
                        rows_to_keep.append(row) #Add game to list of games that aren't being removed

            #write the rest of the rows back
            with open(filename, mode = 'w', newline = '', encoding = 'utf-8') as file:

                                writer = csv.writer(file)
                                #rewrite header row
                                writer.writerow(header)
                                #rewrite filtered rows
                                writer.writerows(rows_to_keep)

            #Create Game instance to use to print confirmation message
            removed_game_instance = cls(removed_game[url_index], removed_game[title_index])

            print(f"{removed_game_instance.title} has been removed")
            
            

    def add_or_remove(cls): 

        """gets user input  about whether do add or remove a game"""

        print("Enter 'a' to add a game, 'r' to remove one, or 'q' to quit the program.")
        user_input = input(str())

        while True:
            if user_input == 'a':
                Game.add_game(Game)
            
            elif user_input == 'r':
                Game.remove_game(Game)
            
            elif user_input == 'q':
                quit()
            else:
                 print("You must enter 'a' to add a game, 'r' to remove one, or 'q' to quit.")

            

if __name__ == "__main__":
    Game.add_or_remove(Game)
    
    
    
    
                                

