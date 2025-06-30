#csv_handler.py
import csv
import os

"""Handles CSV file operations for the application:
- Creating games list CSV file
- Writing game data to CSV (adding, removing, updating)
- Reading game data from CSV"""

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
    
def test_duplicate(url, filename="game_price_list.csv"):
    """Check if the game is already in the csv file"""
    if not os.path.exists(filename):
        return False, None
    else:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if row[header.index('url')] == url:
                    max_price = float(row[header.index('max_price')])
                    return True, max_price
    return False, None

def remove_from_csv(url, filename="game_price_list.csv"):
    """delete a game from the csv file based on its url"""

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
            
            game_exists = False #flag to check game is on csv

            if row[url_index] == url:
                removed_game = row #Store removed game
                game_exists = True #Set flag to true if game is found
                
            else:
                rows_to_keep.append(row) #Add game to list of games that aren't being removed
    
    if game_exists == False:
        #game not found
        pass
    
    else:

        #write the rest of the rows back
            #?? what happens to original file???? 
        with open(filename, mode = 'w', newline = '', encoding = 'utf-8') as file:

                            writer = csv.writer(file)
                            #rewrite header row
                            writer.writerow(header)
                            #rewrite filtered rows
                            writer.writerows(rows_to_keep)

    
