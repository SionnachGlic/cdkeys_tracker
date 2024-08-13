#cdkeys_price_compare

"""Checks the current price of all games on the list against the user's maximum price, sending a desktop notification
if the current price is cheap enough"""

#to read from/write to csv file
import pandas as pd

#to access page to check price
import requests

#to check current price
from bs4 import BeautifulSoup as BS

#to notify
from plyer import notification

def get_new_price(url):
    """Gets the price from the web page"""
    
    page = requests.get(url)

    soup = BS(page.content, 'html.parser')

    #get price
    price_str = soup.find(class_="price").get_text()

    #convert price from string with currency sign to float
    return float(price_str[1:])
        
    

def price_compare(filename = 'game_price_list.csv'):
    
    #make dataframe csv file
    df = pd.read_csv(filename)

    #iterate over each row
    for index, row in df.iterrows():
        #say what each column is using first row's headers
        url = row['url']
        title = row['title']
        current_price = row['current_price']
        max_price = row['max_price']

        #update price from url
        new_price = get_new_price(url)
        df.at[index, 'current_price'] = new_price

        if new_price <= max_price:

            #send desktop notification
            notification.notify(
                title = f"{title}",
                message = (
                    f"{title} now costs £{new_price:.2f}, "
                    f"below the max price of £{max_price:.2f}\n"
                    f"Get it here: {url}"
                    )
                )

    #update csv with new prices
      #save updated prices to csv
    df.to_csv(filename, index = False)

price_compare()

                    
