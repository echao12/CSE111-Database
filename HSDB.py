import sqlite3
from sqlite3 import Error

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

