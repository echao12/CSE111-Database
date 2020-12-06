import sqlite3
from sqlite3 import Error
import csv

class HSDB:
    """
    A class used to manage the Hearthstone database.

    Attributes
    ----------
    conn : sqlite3.Connection
        A connection to the database
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
        
        print ("Creating keywords Table")
        try:
            sql = """CREATE TABLE keywords (
                keyword_key INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_name varchar(10) unique not null,
                keyword_description varchar(25) not null
            )
            """
            self.conn.execute(sql)
            self.conn.commit()
            #print("Success!")
        except Error as e:
            self.conn.rollback()
            print(e)
        try:
            with open('data/keywords.csv', 'r') as keyword_data:
                keyword_reader = csv.reader(keyword_data, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                header = next(keyword_reader)
                print("Header Format: {}".format(header))
                for row in keyword_reader:
                    try:
                        cur = self.conn.cursor()
                        sql = '''insert into keywords (keyword_name, keyword_description) values (?,?)'''
                        args = [row[0], row[1]]
                        cur.execute(sql, args)
                    except Error as e:
                        print("Error inserting keyword {} into keywords table.".format(row[0]))
                        print(e)
                        self.conn.rollback()
            keyword_data.close()
        except Error as e:
            self.conn.rollback()
            print("Error with keyword table creation.")
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
        try:
            print("Creating keyword_cards table")
            self.create_table('keyword_cards', ['keyword_key integer', 'card_key integer'])
        except Error as e:
            print("Error creating keyword_cards table")
            print(e)
        try:
            print("Generating class_cards Table")
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
                            self.checkForKeywords(weapon_cardkey, weapon_text)
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
                            self.checkForKeywords(spell_cardkey, spell_text)
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
                            self.checkForKeywords(cardkey, text)
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
    def checkForKeywords(self, card_key, card_text):
        try:
            sql = '''select keyword_key, keyword_name from keywords'''
            cur = self.conn.cursor()
            cur.execute(sql)
            keywords = cur.fetchall()
            for keyword in keywords:
                #0->key 1->name
                if keyword[1] in card_text:
                    try:
                        print("matching keyword {} - {} - with card_key {}".format(keyword[0], keyword[1], card_key))
                        sql = '''insert into keyword_cards values (?,?)'''
                        args = [keyword[0], card_key]
                        self.conn.execute(sql, args)
                    except Error as e:
                        print("Error inserting a keyword-card_key pair for word:{} card:{}".format(keyword[1], card_key))
                        print(e)
                else:
                    pass
            self.conn.commit()
        except Error as e:
            self.conn.rollback()
            print("Error in keyword search/insert for card {}".format(card_key))
            print(e)
        
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

    def check_card(self, card_name):
        """
        Return True if the given card exists in the database.

        Parameters
        ----------
        card_name : str
            The card name
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM cards WHERE card_name like ?", (card_name,))
            return cursor.fetchone() is not None
        except Error as e:
            print("Error in check_card:", e)
            return False

    def check_class(self, class_name):
        """
        Return True if the given class exists in the database.

        Parameters
        ----------
        class_name : str
            The class name
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM classes WHERE class_name like ?", (class_name,))
            return cursor.fetchone() is not None
        except Error as e:
            print("Error in check_class:", e)
            return False

    def check_hero(self, hero_name):
        """
        Return True if the given hero exists in the database.

        Parameters
        ----------
        hero_name : str
            The hero name
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM heroes WHERE hero_name like ?", (hero_name,))
            return cursor.fetchone() is not None
        except Error as e:
            print("Error in check_hero:", e)
            return False

    def check_card_class(self, card_name, class_name):
        """
        Return True if the given class has access to the given card.

        Parameters
        ----------
        card_name : str
            The card name
        class_name : str
            The class name
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM class_cards 
                              INNER JOIN cards ON cc_cardkey=card_key
                              INNER JOIN classes ON cc_classkey=class_key
                              WHERE card_name like ? AND class_name like ?""", (card_name, class_name,))
            return cursor.fetchone() is not None
        except Error as e:
            print("Error in check_card_class:", e)
            return False

    def check_neutral(self, card_name):
        """
        Return True if the given card is a neutral card.

        Parameters
        ----------
        card_name : str
            The card name
        """

        return self.check_card_class(card_name, "Neutral")

    def check_keyword(self, keyword):
        #will return the keyword if it matches, None if no match
        result = None
        try:
            sql = '''select keyword_name from keywords where keyword_name = "{}"'''.format(keyword)
            cur = self.conn.cursor()
            cur.execute(sql)
            result = cur.fetchone()
        except Error as e:
            print(e)
        
        return result

    def get_cards(self, card_name=None, card_cost=None, card_rarity=None, card_type=None, class_name=None):
        """
        Return the name of all cards that match the given parameters.

        Parameters
        ----------
        card_name : str
            Full or partial card name
        card_cost : int
            Mana cost
        card_rarity : str
            Rarity, must be one of "Free", "Common", "Rare", "Epic", or "Legendary"
        card_type : str
            Type of card, must be one of "Minion", "Spell", or "Weapon"
        class_name : str
            Name of the class
        """

        try:
            # Construct SQL query
            sql_where = "WHERE"
            sql_parameters = ()
            
            # card_name
            if card_name is not None:
                sql_where += " card_name like ?"
                sql_parameters += ("%" + card_name + "%",)
            
            # card_cost
            if card_cost is not None:
                if len(sql_where) > 5:
                    sql_where += " AND"
                sql_where += " card_cost = ?"
                sql_parameters += (card_cost,)

            # card_rarity
            if card_rarity is not None:
                if len(sql_where) > 5:
                    sql_where += " AND"
                sql_where += " card_rarity like ?"
                sql_parameters += (card_rarity,)

            # card_type
            if card_type is not None:
                if len(sql_where) > 5:
                    sql_where += " AND"
                sql_where += " card_type like ?"
                sql_parameters += (card_type,)

            # class_name
            if class_name is not None:
                if len(sql_where) > 5:
                    sql_where += " AND"
                sql_where += " class_name like ?"
                sql_parameters += (class_name,)

            # Create cursor
            cursor = self.conn.cursor()
            
            # Execute query
            if len(sql_where) > 5:
                cursor.execute("""SELECT DISTINCT card_name FROM cards
                                  INNER JOIN class_cards ON card_key=cc_cardkey
                                  INNER JOIN classes ON cc_classkey=class_key
                                  """ + sql_where, sql_parameters)
            else:
                cursor.execute("SELECT card_name FROM cards")
            
            # Get all of the matching rows
            result = cursor.fetchall()
            
            # Return result as a list (of card names)
            return [res[0] for res in result]

        except Error as e:
            print("Error in get_cards:", e)
            return []

    def get_heroes(self, hero_name=None, class_name=None):
        """
        Return the name of all heroes that match the given parameters.

        Parameters
        ----------
        hero_name : str
            Full or partial hero name
        class_name : str
            Name of the class
        """

        try:
            # Construct SQL query
            sql_where = "WHERE"
            sql_parameters = ()
            
            # hero_name
            if hero_name is not None:
                sql_where += " hero_name like ?"
                sql_parameters += ("%" + hero_name + "%",)
            
            # class_name
            if class_name is not None:
                if len(sql_where) > 5:
                    sql_where += " AND"
                sql_where += " class_name like ?"
                sql_parameters += (class_name,)

            # Create cursor
            cursor = self.conn.cursor()
            
            # Execute query
            if len(sql_where) > 5:
                cursor.execute("""SELECT hero_name FROM heroes
                                  INNER JOIN classes ON hero_classkey=class_key
                                  """ + sql_where, sql_parameters)
            else:
                cursor.execute("SELECT hero_name FROM heroes")
            
            # Get all of the matching rows
            result = cursor.fetchall()
            
            # Return result as a list (of hero names)
            return [res[0] for res in result]

        except Error as e:
            print("Error in get_heroes:", e)
            return []

    def get_hero_class(self, hero_name):
        """
        Return the class of the given hero.

        Parameters
        ----------
        hero_name : str
            The hero name
        """

        if self.check_hero(hero_name) == False:
            print(hero_name, "does not exist in the database")
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT class_name FROM classes
                              INNER JOIN heroes ON class_key=hero_classkey
                              WHERE hero_name = ?""", (hero_name,))
            return cursor.fetchone()[0]
        except Error as e:
            print("Error in get_hero_class:", e)
            return None

    def get_card_statistics(self, card_name):
        """
        Return the statistics of the given card.

        Parameters
        ----------
        card_name : str
            The card name
        """

        # Make sure the card exists in the database
        if self.check_card(card_name) == False:
            print(card_name, "does not exist in the database")
            return None

        try:
            # Initialize an empty dictionary for the statistics
            stats = {}

            # Get the type of the card
            cursor = self.conn.cursor()
            cursor.execute("""SELECT card_type FROM cards
                              WHERE card_name = ?""", (card_name,))
            card_type = cursor.fetchone()[0]
            stats["type"] = card_type
            
            if card_type == "Minion":
                # Get all minion-related attributes
                cursor.execute("""SELECT card_name, card_rarity, card_cost, minion_text, minion_attack, minion_health
                                  FROM cards
                                  INNER JOIN minions ON card_key = minion_cardkey
                                  WHERE card_name = ?""", (card_name,))
                card = cursor.fetchone()
                stats["minion_name"] = card[0]
                stats["minion_rarity"] = card[1]
                stats["minion_cost"] = card[2]
                stats["minion_text"] = card[3]
                stats["minion_attack"] = card[4]
                stats["minion_health"] = card[5]

            elif card_type == "Spell":
                # Get all spell-related attributes
                cursor.execute("""SELECT card_name, card_rarity, card_cost, spell_text
                                  FROM cards
                                  INNER JOIN spells ON card_key = spell_cardkey
                                  WHERE card_name = ?""", (card_name,))
                card = cursor.fetchone()
                stats["spell_name"] = card[0]
                stats["spell_rarity"] = card[1]
                stats["spell_cost"] = card[2]
                stats["spell_text"] = card[3]
            
            elif card_type == "Weapon":
                # Get all weapon-related attributes
                cursor.execute("""SELECT card_name, card_rarity, card_cost, weapon_text, weapon_attack, weapon_durability
                                  FROM cards
                                  INNER JOIN weapons ON card_key = weapon_cardkey
                                  WHERE card_name = ?""", (card_name,))
                card = cursor.fetchone()
                stats["weapon_name"] = card[0]
                stats["weapon_rarity"] = card[1]
                stats["weapon_cost"] = card[2]
                stats["weapon_text"] = card[3]
                stats["weapon_attack"] = card[4]
                stats["weapon_durability"] = card[5]

            # Return the statistics
            return stats

        except Error as e:
            print("Error in get_card_statistics:", e)
            return None
            
    def viewCardsByKeyword(self, keywords):
        print("Checking for cards with these keywords: {}".format(keywords))
        cardList = []
        try:
            cursor = self.conn.cursor()
            for keyword in keywords:
                print("Searching for keyword: {}".format(keyword))
                sql = '''select cardkey, card_name, text, keyword_name, keyword_description 
                            from keywords, keyword_cards, (select minion_cardkey as cardkey, card_name,  minion_text as text from minions, cards on minion_cardkey = card_key
                                                            UNION
                                                            select spell_cardkey, card_name, spell_text from spells, cards on spell_cardkey = card_key
                                                            UNION
                                                            select weapon_cardkey, card_name, weapon_text from weapons, cards on weapon_cardkey = card_key
                                                            )
                            on cardkey = keyword_cards.card_key and keywords.keyword_key = keyword_cards.keyword_key
                            where keyword_name = "{}"'''.format(keyword)
                #print(sql)
                cursor.execute(sql)
                for row in cursor:
                    cardList.append(row)
            print("Search Results:")
            print("{:<10} {:<25} {:<125} {:<15}".format("card_key","card_name", "card_text", "keyword"))
            for card in cardList:
                #print(card[0])
                print("{:<10} {:<25} {:<125} {:<15}".format(card[0], card[1], card[2], card[3]))
        except Error as e:
            print(e)
        return cardList