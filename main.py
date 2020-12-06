import pandas as pd
from HSDB import HSDB
from Deck import Deck

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
    db.drop_table("keywords")
    db.drop_table("keyword_cards")
    #db.generateMinions() #testing minion table generation
    #db.generateSpells() #testing spell table generation
    #db.generateWeapons() #testing weapon table generation

    # this fn will generate and populate Heroes, Classes, Cards, and other related tables
    # for use from the cards/classes/heroes csv files.
    db.create_tables_from_data(cards, heroes)

    #Generate sample deck from text file
    sample_deck = Deck(db)
    sample_deck.generate_deck_from_text_file("data/sample_deck_1.txt")
    print("Sample Deck:")
    print(sample_deck)
    
    # Print sample deck statistics
    sample_deck_stats = sample_deck.get_deck_statistics()
    for key in sample_deck_stats:
        print(key, sample_deck_stats[key])
    print("\n")

    # Generate random deck
    print("Random Deck:")
    random_deck = Deck(db)
    random_deck.randomize()
    print(random_deck)
    
    # Print random deck statistics
    random_deck_stats = random_deck.get_deck_statistics()
    for key in random_deck_stats:
        print(key, random_deck_stats[key])

if __name__ == '__main__':
    main()
