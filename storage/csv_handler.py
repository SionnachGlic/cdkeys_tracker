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
        writer.writerow([self.url, self.title, self.current_price, self.max_price])
    
def test_duplicate(url, filename="game_price_list.csv"):
    """Check if the game is already in the csv file"""
    if not os.path.exists(filename):
        return False, None #if the file doesn't exist then no duplicates
    else:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            try:
                header = next(reader)
                print
            #if csv is empty, then theres no duplicate
            except StopIteration:
                return False, None

            for row in reader:
                if row[header.index('url')].strip() == url.strip():
                    current_max_price = float(row[header.index('max_price')])
                    return True, current_max_price
    return False, None

def csv_update_max_price(url: str, updated_price: float, filename="game_price_list.csv"):
     """Update the price of a game."""
     #read csv to find row that has url
     with open(filename, mode = 'r', newline = '', encoding = 'utf-8') as file:
          reader = csv.reader(file)
          #store rows as list
          rows = list(reader)

          #extracts first row and stores it in variable called header
          #not gonna try/except StopIteration because this function is only called if at least 1 game exists
          header = rows[0]

          #index url and max_price to compare and update respectively
          url_index = header.index('url')
          max_price_index = header.index('max_price')

          #find row with matching url and update max_price
          for i in range(1, len(rows)):
              if rows[i][url_index].strip() == url.strip():
                  rows[i][max_price_index] = updated_price
                  break

     #write all rows back to csv file   
     with open(filename, mode = 'w', newline = '', encoding = 'utf-8') as file:
         writer = csv.writer(file)
         writer.writerow(header) #write header row
         writer.writerows(rows[1:]) #write the rest of the rows
    

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

        game_exists = False #flag to check game is on csv
        
        for row in reader:

            if row[url_index].strip() == url.strip():
                removed_game = row #Store removed game
                game_exists = True #Set flag to true if game is found
                
            else:
                rows_to_keep.append(row) #Add game to list of games that aren't being removed
    
    if game_exists == False:
        #game not found - need to do something here, will probably sort when doing GUI
        pass
    
    else:

        #write the rest of the rows back
        with open(filename, mode = 'w', newline = '', encoding = 'utf-8') as file:

                            writer = csv.writer(file)
                            #rewrite header row
                            writer.writerow(header)
                            #rewrite filtered rows
                            writer.writerows(rows_to_keep)

    
