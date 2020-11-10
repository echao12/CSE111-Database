import pandas as pd
from HSDB import HSDB

def main():
    # Read in the data
    cards = pd.read_csv('data/cards.csv')
    heroes = pd.read_csv('data/heroes.csv')

    # Initialize a database manager and establish connection to the database
    db = HSDB()
    db.connect('data/hs.sqlite')

    # Drop all tables
    db.drop_table("Cards")
    db.drop_table("Classes")
    db.drop_table("Heroes")

    
    db.drop_table("spells")
    db.drop_table("minions")
    db.drop_table("class_cards")
    db.drop_table("weapons")
    #db.generateMinions() #testing minion table generation
    #db.generateSpells() #testing spell table generation
    #db.generateWeapons() #testing weapon table generation

    # Do stuff
    # this fn will generate and populate Heroes, Classes, Cards, and other related tables
    # for use from the cards/classes/heroes csv files.
    db.create_tables_from_data(cards, heroes)

if __name__ == '__main__':
    main()
