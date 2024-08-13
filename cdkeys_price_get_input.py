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
    
    def __init__(self, url, title, price_float, max_price):
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
        

    def scrape_title(url):
        """Gets the title from the web page"""
    
        page = requests.get(url)

        soup = BS(page.content, 'html.parser')

        #Get title of page
        title = soup.find(class_="page-title").get_text()
        
        return title


    def scrape_price(url):
        """Gets the price from the web page"""
    
        page = requests.get(url)

        soup = BS(page.content, 'html.parser')
        
        #get price
        price_str = soup.find(class_="price").get_text()
        
        #convert price from string with currency sign to float
        price_float = float(price_str[1:])
        
        return price_float
        
    def product_details(cls):
        """allows the user to input the game's url and their max price"""
        
        print("Enter q to quit at any time")
        user_input = ""

        #create infinite loop, not while loop, because it'll try to scrape
        #from 'q' before ending the loop. instead use break
        
        while True:

            print()
            print("What is the URL of the product you want to track?")
            user_input = input(str())
            
            #break if user quits
            if user_input == 'q':
                break

            
            url = user_input
            title = cls.scrape_title(url)
            price_float = cls.scrape_price(url)

            print()
            print(f"The current price of {title} is £{price_float:.2f}.")
            
            print()
            print("What is the maximum price you're willing to pay for this?")
            user_input = input("£")
            
            if user_input == 'q':
                break
            
            max_price = float(user_input)

            #add this one to csv
            game_instance = cls(url, title, price_float, max_price)
            game_instance.save_to_csv()
            print()
            print("Game information saved")
            

if __name__ == "__main__":
    Game.product_details(Game)

