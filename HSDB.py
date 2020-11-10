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
            print("sql = {}".format(sql_statement))
            self.conn.execute(sql_statement)
        except Error as e:
            print("Error in create_table:", e)

    #TODO: Link the individual table creations to use the create_table() fn to prevent overwrite each time we run
    #and then have them individually populate when needed
    #for now, we just gatta make it work lol
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
            sql = """CREATE TABLE cards (
                card_key INTEGER PRIMARY KEY AUTOINCREMENT,
                card_name varchar(25) not null,
                card_cost integer,
                card_rarity varchar(10) not null,
                card_type varchar(10) not null)"""
            self.conn.execute(sql)
            self.conn.commit()
            print("Success!")
        except Error as e:
            self.conn.rollback()
            print(e)

        print("Creating class Table")
        try:
            args = ["class_key integer primary key autoincrement","class_name varchar(15) not null"]
            #self.create_table("Classes", "class_key primary key autoincrement, class_name varchar(15) not null")
            self.create_table("classes", args)
            print("Populating classes Table")
            try:
                with open('data/classes.csv', 'r') as classData:
                    classReader = csv.reader(classData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                    header = next(classReader)
                    print("Header Format: {}".format(header))
                    #sql = """INSERT INTO {} (class_name) VALUES (?)""".format("Classes")
                    #print(sql)
                    #note: classes csv format: class_name
                    for row in classReader:
                        sql = """INSERT INTO {} (class_name) VALUES(?)""".format("classes")
                        #print(sql)
                        args = [row[0]]
                        #print("before execute")
                        self.conn.execute(sql, args)
                        #print("after execute")
                        self.conn.commit()
                    #print("after commit")
                classData.close()
            except Error as e:
                print("Error Opening classes.csv or inserting class to table")
                self.conn.rollback()
                print(e)

        except Error as e:
            print("Error Creating/Populating class Table")
            print(e)



        print ("Creating heroes Table")
        try:
            sql = """CREATE TABLE heroes (
                hero_classkey integer,
                hero_name varchar(20) not null,
                hero_power_name varchar(15) not null,
                hero_power_cost integer,
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
        print("Importing cards data...")
        try:
            with open('data/cards.csv', 'r') as cardData:
                cardReader = csv.reader(cardData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(cardReader)
                print("Header Format: {}".format(header))
                #cards csv format ['Name', 'Type', 'Rarity', 'Cost', 'Attack', 'Health', 'Text', 'Classes']
                for row in cardReader:
                    #print(row)
                    self.insertCardToTable("cards", row[0], row[3], row[2], row[1])
            cardData.close()
            print("Done Reading In cards Data\n")
        except Error as e:
            self.conn.rollback()
            print(e)
        
        print("Importing heroes Data...")
        try:
            with open('data/heroes.csv', 'r') as heroData:
                heroReader = csv.reader(heroData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(heroReader)
                print("Header Format: {}".format(header))
                #heroes csv format ['Name', 'Hero Power Name', 'Hero Power Cost', 'Hero Power Text', 'Class']
                for row in heroReader:
                    #print(row)
                    self.insertHeroToTable("heroes", row[0], row[1], row[2], row[3], row[4])
            heroData.close()
            print("Done reading/inserting hero data...\n")
        except Error as e:
            print(e)

        print("Creating all relational tables for cards/heroes...\n")
        print("Generating class_cards Table")
        try:
            self.generateClassCardsTable()
        except Error as e:
            print("ERROR in generating class_cards Table!")
            print(e)
        try:
            self.generateMinions()
        except Error as e:
            print("error generating minions Table")
            print(e)
        try:
            self.generateSpells()
        except Error as e:
            print("Error generating spells table")
            print(e)
        try:
            self.generateWeapons()
        except Error as e:
            print("Error generating weapons table")
            print(e)
        print("*** Finished generating all tables using data from the cards/classes/heroes csv files***\n")
        
    def generateWeapons(self):
        print("Begin generating weapons table...")
        try:
            self.create_table('weapons', ['weapon_cardkey integer', 'weapon_attack integer', 'weapon_durability integer', 'weapon_text varchar(25) not null'])
        except Error as e:
            print("Error creating weapons table...")
            print(e)
        try:
            with open("data/cards.csv", 'r') as cardData:
                cardReader = csv.reader(cardData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(cardReader)
                #cards csv format ['Name', 'Type', 'Rarity', 'Cost', 'Attack', 'Health', 'Text', 'Classes']
                print(header)
                for card in cardReader:
                    #minions format: cardkey, attack, health, text
                    if card[1] != 'Weapon':
                        continue 
                    else:
                        try:
                            sql = '''select card_key from cards where card_name = "{}"'''.format(card[0])
                            cur = self.conn.cursor()
                            cur.execute(sql)
                            weapon_cardkey = cur.fetchone()
                            weapon_cardkey = weapon_cardkey[0]
                            weapon_attack = card[4]
                            weapon_durability = card[5]
                            weapon_text = card[6]
                            sql = '''Insert INTO {}(weapon_cardkey, weapon_attack, weapon_durability, weapon_text) values (?,?,?,?)'''.format("weapons")
                            args = [weapon_cardkey, weapon_attack, weapon_durability, weapon_text]
                            #print(sql)
                            self.conn.execute(sql, args)
                            self.conn.commit()
                        except Error as e:
                            self.conn.rollback()
                            print("Error inserting weapon {} into weapons table".format(card[0]))
                            print(e)
            cardData.close()
            print("SUCCESS!")
        except Error as e:
            print("ERROR reading/inserting weapon cards into weapons table")
        print("Completed weapons table generation...\n")






    def generateSpells(self):
        print("Begin generating spells table...")
        try:
            self.create_table('spells', ['spell_cardkey integer', 'spell_text varchar(25) not null'])
        except Error as e:
            print("Error creating spells table...")
            print(e)
        try:
            with open("data/cards.csv", 'r') as cardData:
                cardReader = csv.reader(cardData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(cardReader)
                #cards csv format ['Name', 'Type', 'Rarity', 'Cost', 'Attack', 'Health', 'Text', 'Classes']
                print(header)
                for card in cardReader:
                    #minions format: cardkey, attack, health, text
                    if card[1] != 'Spell':
                        continue 
                    else:
                        try:
                            sql = '''select card_key from cards where card_name = "{}"'''.format(card[0])
                            cur = self.conn.cursor()
                            cur.execute(sql)
                            spell_cardkey = cur.fetchone()
                            spell_cardkey = spell_cardkey[0]
                            spell_text = card[6]
                            sql = '''Insert INTO {}(spell_cardkey, spell_text) values (?,?)'''.format("spells")
                            args = [spell_cardkey, spell_text]
                            #print(sql)
                            self.conn.execute(sql, args)
                            self.conn.commit()
                        except Error as e:
                            self.conn.rollback()
                            print("Error inserting spell {} into spells table".format(card[0]))
                            print(e)
            cardData.close()
            print("SUCCESS")
        except Error as e:
            print("ERROR reading/inserting spells into spell table")
        
        print("Completed spells table generation...\n")


    def generateMinions(self):
        print("Begin generating minions table...")
        try:
            self.create_table('minions', ['minion_cardkey integer', 'minion_attack integer', 'minion_health integer', 'minion_text varchar(25) not null'])
        except Error as e:
            print("Error creating minions table...")
            print(e)
        try:
            with open("data/cards.csv", 'r') as cardData:
                cardReader = csv.reader(cardData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(cardReader)
                #cards csv format ['Name', 'Type', 'Rarity', 'Cost', 'Attack', 'Health', 'Text', 'Classes']
                print(header)
                for card in cardReader:
                    #minions format: cardkey, attack, health, text
                    if card[1] != 'Minion':
                        continue 
                    else:
                        print(card)
                        try:
                            attack = card[4]
                            health = card[5]
                            text = card[6]
                            sql = '''select card_key from Cards where card_name = "{}"'''.format(card[0])
                            cur = self.conn.cursor()
                            cur.execute(sql)
                            cardkey = cur.fetchone()
                            cardkey = cardkey[0]
                            #print("cardkey:{} | health:{} | text:{} | {}".format(cardkey, health, attack, text))
                            sql = '''INSERT INTO {}(minion_cardkey, minion_attack, minion_health, minion_text) values (?,?,?,?)'''.format('minions')
                            args = [cardkey, attack, health, text]
                            self.conn.execute(sql, args)
                            self.conn.commit()
                        except Error as e:
                            print("ERROR inserting {} into minion table...".format(card[0]))
                            self.conn.rollback()
                            print(e)
            cardData.close()
            print("SUCCESS!")
        except Error as e:
            print(e)
        print("Done generating minion table...\n")


    
                    

    def generateClassCardsTable(self):
        #will match up cardkey to corresponding classkey
        #must open cards.csv to get class name
        #fetch card name and card class from .csv getch card key from Cards & fetch class key from Classes
        try:
            self.create_table("class_cards", ["cc_cardkey integer", "cc_classkey integer"])
        except Error as e:
            print("ERROR in creating class_cards")
            print(e)
        
        try:
            with open('data/cards.csv', 'r') as cardData:
                cardReader = csv.reader(cardData, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(cardReader)
                #cards csv format ['Name', 'Type', 'Rarity', 'Cost', 'Attack', 'Health', 'Text', 'Classes']
                for card in cardReader:
                    card_name = card[0]
                    card_classes = card[7].split("|")
                    #print("got card class/name")
                    sql = '''select card_key from cards where card_name = "{}"'''.format(card_name)
                    cur = self.conn.cursor()
                    cur.execute(sql) #get card_key from cards table
                    values = cur.fetchone()
                    card_key = values[0]
                    #print("got card key")
                    #print("Class Key Values:")
                    for card_class in card_classes:
                        sql = '''select class_key from classes where class_name = "{}"'''.format(card_class)
                        cur = self.conn.cursor()
                        cur.execute(sql)
                        card_class_val = cur.fetchone()
                        #print(card_class_val[0])
                    #for cardclass in cardclasses:
                    #    print(cardclass)
                    #card_classkey = values[0]
                        #print("got card class key")
                        #print("card name: {} | card key: {} | class: {} | classkey: {}\n".format(card_name, card_key, card_class, card_class_val[0]))
                        try:
                            sql = '''Insert into {} (cc_cardkey, cc_classkey) values ({},{})'''.format('class_cards', card_key, card_class_val[0])
                            #print(sql)
                            self.conn.execute(sql)
                            self.conn.commit()
                        except Error as e:
                            print("Failed to insert class_cards entry for {}".format(card_name))
                            print(e)
                            self.conn.rollback()
            cardData.close()
            print("SUCCESS!")
        except Error as e:
            print(e)
        print("Finished generating class_card table!\n")

                    
                    




    
    #TODO: Need to finish vvv and classes table
    def insertHeroToTable(self, table, hero_name, hero_power_name, hero_power_cost, hero_power_text, hero_class):
        #print("Inserting hero {} to table...".format(hero_name))
        try:
            sql = """INSERT INTO {} (hero_classkey, hero_name, hero_power_name, hero_power_cost, hero_power_text) VALUES (?,?,?,?,?)""".format(table)
            classKeyValSQL = """select class_key from classes where class_name = '{}'""".format(hero_class)
            #print(sql)
            try:
                cur = self.conn.cursor()
                cur.execute(classKeyValSQL) #extract the classkey from the classes database
                classKeyVal = cur.fetchone()
                classKeyVal = classKeyVal[0]#remove the ',' at the end
                #print("classkey for {} who is a {} is {}".format(hero_name, hero_class, classKeyVal))

            except Error as e:
                print("Error extracting class key for {}".format(hero_name))
                print(e)

            args = [classKeyVal, hero_name, hero_power_name, hero_power_cost, hero_power_text]
            self.conn.execute(sql,args)
            self.conn.commit()

        except Error as e:
            print("*Error inserting {} into hero table...".format(hero_name))
            print(e)

    def insertCardToTable(self, table, card_name, card_cost, card_rarity, card_type):
        #print("Inserting card to table...")
        try:
            sql = """INSERT INTO {} (card_name, card_cost, card_rarity, card_type) VALUES(?,?,?,?)""".format(table)
            args = [card_name, card_cost, card_rarity, card_type]
            self.conn.execute(sql, args)
            self.conn.commit()
        except Error as e:
            self.conn.rollback()
            print(e)
        #print("Done inserting card data to table...")

        
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

