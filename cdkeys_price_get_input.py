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
        """Gets the title from the web page"""
    
        page = requests.get(url)

        soup = BS(page.content, 'html.parser')

        #Get title of page
        title = soup.find(class_="page-title").get_text()
        
        return title

    @staticmethod
    def scrape_price(url):
        """Gets the price from the web page"""
    
        page = requests.get(url)

        soup = BS(page.content, 'html.parser')
        
        #get price
        price_str = soup.find(class_="price").get_text()
        
        #convert price from string with currency sign to float
        price_float = float(price_str[1:])
        
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
    
    
    
    
                                

