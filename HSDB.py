import sqlite3
from sqlite3 import Error
import csv

class HSDB:
    """
    A class used to manage the Hearthstone database.
    """

    def __init__(self):
        """
        Constructor
        """

        self.conn = None

    def connect(self, db_file):
        """
        Establish a connection the a database.

        Parameters
        ----------
        db_file : str
            The path to the database (.sqlite) file
        """

        self.conn = sqlite3.connect(db_file)

    def create_table(self, name, fields):
        """
        Create a new table in the database.

        Parameters
        ----------
        name : str
            The name of the table
        fields : list of str
            The columns of the table, which include name, type, and other optional arguments
        """

        try:
            sql_statement = "CREATE TABLE IF NOT EXISTS " + name + " (" + ", ".join(fields) + ");"
            self.conn.execute(sql_statement)
        except Error as e:
            print("Error in create_table:", e)

    def create_tables_from_data(self, cards, heroes):
        """
        Create tables from a given data.

        Parameters
        ----------
        cards : Pandas.DataFrame
            A Pandas DataFrame object consisting of Hearthstone cards. The DataFrame must have
            the following columns:
                - Name (str)
                - Type (str)
                - Rarity (str)
                - Cost (int)
                - Attack (int or NaN)
                - Health (int or NaN)
                - Text (str)
                - Classes (str)

        heroes : Pandas.DataFrame
            A Pandas DataFrame object consisting of Hearthstone heroes. The DataFrame must have
            the following columns:
                - Name (str)
                - Hero Power Name (str)
                - Hero Power Cost (int)
                - Hero Power Text (str)
                - Class (str)
        """
        # TODO: Create and populate tables: cards, minions, spells, weapons, classes, heroes, classcards
        print("Creating Cards Table\n")
        try:
            sql = """CREATE TABLE Cards (
                card_key INTEGER PRIMARY KEY AUTOINCREMENT,
                card_name varchar(25) not null,
                card_cost decimal(2,0),
                card_rarity varchar(10) not null,
                card_type varchar(10) not null)"""
            self.conn.execute(sql)
            self.conn.commit()
            print("Success!")
        except Error as e:
            self.conn.rollback()
            print(e)

        #print("Creating Class Table")
        #try:
        #    self.create_table("Classes", "class_key, class_name")

        print ("Creating Heroes Table")
        try:
            sql = """CREATE TABLE Heroes (
                hero_classkey decimal(2,0),
                hero_name varchar(20) not null,
                hero_power_cost decimal(2,0),
                hero_power_text varchar(50)
            )
            """
            self.conn.execute(sql)
            self.conn.commit()
            print("Success!")
        except Error as e:
            self.conn.rollback()
            print(e)
        
        print("Starting to import data...")
        print("Importing Cards data...")
        try:
            with open('data/cards.csv', 'r') as cardData:
                cardReader = csv.reader(cardData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(cardReader)
                print("Header Format: {}".format(header))
                #cards csv format ['Name', 'Type', 'Rarity', 'Cost', 'Attack', 'Health', 'Text', 'Classes']
                for row in cardReader:
                    print(row)
                    self.insertCardToTable("Cards", row[0], row[3], row[2], row[1])

            print("Done Reading In Cards Data")
        except Error as e:
            self.conn.rollback()
            print(e)
        
        print("Importing Heroes Data...")
        try:
            with open('data/heroes.csv', 'r') as heroData:
                heroReader = csv.reader(heroData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(heroReader)
                print("Header Format: {}".format(header))
                #heroes csv format ['Name', 'Hero Power Name', 'Hero Power Cost', 'Hero Power Text', 'Class']
                for row in heroReader:
                    print(row)
                    #self.insertHeroToTable()
            print("Done reading Hero data...")
        except Error as e:
            print(e)
    
    def insertCardToTable(self, table, card_name, card_cost, card_rarity, card_type):
        print("Inserting card to table...")
        try:
            sql = """INSERT INTO {} (card_name, card_cost, card_rarity, card_type) VALUES(?,?,?,?)""".format(table)
            args = [card_name, card_cost, card_rarity, card_type]
            self.conn.execute(sql, args)
            self.conn.commit()
        except Error as e:
            self.conn.rollback()
            print(e)
        #print("Done inserting card data to table...")
    
    #TODO: Need to finish vvv and classes table
    def insertHeroToTable(self, table, hero_name, hero_power_name, hero_power_text, hero_class):
        print("Inserting hero to table...")
        #try:
        #    sql = """"INSERT INTO {} ("""
        
    def drop_table(self, name):
        """
        Drop a table in the database.

        Parameters
        ----------
        name : str
            The name of the table
        """

        try:
            sql_statement = "DROP TABLE IF EXISTS " + name + ";"
            self.conn.execute(sql_statement)
        except Error as e:
            print("Error in drop_table:", e)

