import pandas as pd
from HSDB import HSDB

def main():
    # Read in the data
    cards = pd.read_csv('data/cards.csv')
    heroes = pd.read_csv('data/heroes.csv')

    # Initialize a database manager and establish connection to the database
    db = HSDB()
    db.connect('data/hs.sqlite')

    # Create tables
    #db.drop_table("Cards")
    db.drop_table("Classes")
    db.drop_table("Heroes")
    #this will generate the base Heroes, Classes, Cards, and other related tables for use.
    db.create_tables_from_data(cards, heroes)
    

    # Do stuff

if __name__ == '__main__':
    main()
