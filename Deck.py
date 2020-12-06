import string
import random

class Deck:
    """
    A class used to represent a Hearthstone deck.

    Attributes
    ----------
    db : HSDB
        A reference to the Hearthstone database
    name : str
        The name of the deck
    hero : str
        The name of the hero
    hero_class : str
        The class of the hero
    cards : list of str
        A list of card names
    """

    def __init__(self, db, name=None, hero=None, cards=[]):
        """
        Constructor
        """

        self.db = db
        self.name = None
        self.hero = None
        self.hero_class = None
        self.cards = []
        
        if name is not None:
            self.set_name(name)
        
        if hero is not None:
            self.set_hero(hero)

        if len(cards) > 0:
            self.set_cards(cards)

    def set_name(self, name):
        """
        Change the name of the deck.

        Parameters
        ----------
        name : str
            The new name for the deck
        """

        self.name = name

    def set_hero(self, hero):
        """
        Change the hero of the deck. This will remove all of the cards in the deck.
        Return True if the hero is a valid hero, return False otherwise.

        Parameters
        ----------
        hero : str
            The new hero
        """

        if self.db.check_hero(hero):
            self.hero = hero
            self.hero_class = self.db.get_hero_class(hero)
            self.cards = []
            return True
        else:
            print(hero, "is not a valid hero!")
            return False

    def set_cards(self, cards):
        """
        Change the entire cards of the deck. Return True if all cards are successfully 
        added to the deck, return False otherwise.

        Parameters
        ----------
        cards : list of str
        """

        if self.hero is None:
            print("Deck does not have a hero")
            return False

        if len(cards) > 30:
            print("Too many cards")
            return False

        for card in cards:
            if self.db.check_card(card) is False:
                print(card, "is not a valid card")
                return False
            elif self.db.check_card_class(card, self.hero_class) is False:
                print(card, "does not fit the deck's class")
                return False

        # TODO? Implement card limit based on the rarity of the card
        self.cards = [card for card in cards]

        return True

    def add_card(self, card_name):
        """
        Add a card to the deck. Return True if the operation is successful, return
        False otherwise.
        """

        if self.hero is None:
            print("Deck does not have a hero")
            return False

        if len(self.cards) == 30:
            print("Deck is full")
            return False

        if self.db.check_card(card_name) is False:
            print(card_name, "is not a valid card")
            return False

        if self.db.check_neutral(card_name) is False and self.db.check_card_class(card_name, self.hero_class) is False:
            print(card_name, "does not fit the class of the deck")
            return False

        # TODO? Implement card limit based on the rarity of the card
        self.cards.append(card_name)
        
        return True

    def remove_card(self, card_name):
        """
        Remove a card from the deck.
        """

        self.cards.remove(card_name)

    def check_card(self, card_name):
        """
        Check if a card is in the deck.
        """

        return card_name in self.cards

    def get_deck_statistics(self):
        """
        Get deck statistics. This includes:
            - Deck name (str)
            - Hero name (str)
            - Class name (str)
            - Number of cards (int)
            - Number of minions (int)
            - Number of spells (int)
            - Number of weapons (int)
            - Mana curve (list of int)
            - Rarity count (dict)
        """

        deck_stats = {}
        deck_stats["deck_name"] = self.name
        deck_stats["hero_name"] = self.hero
        deck_stats["class_name"] = self.hero_class
        deck_stats["num_cards"] = len(self.cards)
        deck_stats["num_minions"] = 0
        deck_stats["num_spells"] = 0
        deck_stats["num_weapons"] = 0
        deck_stats["mana_curve"] = [0] * 12  # 0,1,2,3,4,5,6,7,8,9,10,>10
        deck_stats["rarity_count"] = {}
        deck_stats["rarity_count"]["Free"] = 0
        deck_stats["rarity_count"]["Common"] = 0
        deck_stats["rarity_count"]["Rare"] = 0
        deck_stats["rarity_count"]["Epic"] = 0
        deck_stats["rarity_count"]["Legendary"] = 0

        for card_name in self.cards:
            card_stats = self.db.get_card_statistics(card_name)
            
            if card_stats["type"] == "Minion":
                deck_stats["num_minions"] += 1
                mana_cost = card_stats["minion_cost"]
                rarity = card_stats["minion_rarity"]

            elif card_stats["type"] == "Spell":
                deck_stats["num_spells"] += 1
                mana_cost = card_stats["spell_cost"]
                rarity = card_stats["spell_rarity"]

            elif card_stats["type"] == "Weapon":
                deck_stats["num_weapons"] += 1
                mana_cost = card_stats["weapon_cost"]
                rarity = card_stats["weapon_rarity"]

            if mana_cost <= 10:
                deck_stats["mana_curve"][mana_cost] += 1
            else:
                deck_stats["mana_curve"][11] += 1  # for anything above 10 mana

            deck_stats["rarity_count"][rarity] += 1

        return deck_stats

    def print_deck_statistics(self):
        if self.name is None or self.hero is None or self.hero_class is None or len(self.cards) == 0:
            print("Deck is incomplete")
        else:
            stats = self.get_deck_statistics()
            print("Deck Statistics")
            print("Hero:", stats["hero_name"])
            print("Class:", stats["class_name"])
            print("Number of cards:", stats["num_cards"])
            print("")
            print("{:<7} {:<7} {:<7} {:<7}".format("Type", "Minion", "Spell", "Weapon"))
            print("{:<7} {:<7} {:<7} {:<7}".format("Count", stats["num_minions"], stats["num_spells"], stats["num_weapons"]))
            print("")
            for i in range(max(stats["mana_curve"]), 0, -1):
                asterisks = ["*" if count >= i else "" for count in stats["mana_curve"]]
                print("{:<6} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4}".format("", *asterisks))
            print("{:<6} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4}".format("Mana", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "11+"))
            print("{:<6} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4}".format("Count", *stats["mana_curve"]))
            print("")
            print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<10}".format("Rarity", "Free", "Common", "Rare", "Epic", "Legendary"))
            print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format("Count", stats["rarity_count"]["Free"], stats["rarity_count"]["Common"], stats["rarity_count"]["Rare"], stats["rarity_count"]["Epic"], stats["rarity_count"]["Legendary"]))
            print("")

    def randomize(self, name=None, hero=None, hero_class=None, card_count=30):
        """
        Randomize the content of the deck.

        Parameters
        ----------
        name : str
            If not None, set this as the deck name, otherwise set a random name
        hero : str
            If not None, set this as the deck hero, otherwise choose a random hero
        hero_class : str
            If not None, choose a random hero from this class ('hero' argument must be None),
            otherwise choose a random class
        """

        # Set deck name
        if name is not None:
            self.name = name
        else:
            self.name = ""
            for _ in range(3):
                self.name += random.choice(string.ascii_uppercase)
            self.name += " "
            self.name += str(random.randint(1,1000))

        # Set deck hero
        if hero is not None:
            if self.set_hero(hero) == False:
                return
        else:
            valid_heroes = []

            if hero_class is not None:
                if self.db.check_class(hero_class):
                    valid_heroes = self.db.get_heroes(hero_class=hero_class)
                else:
                    print(hero_class, "is not a valid class")
                    return
            else:
                valid_heroes = self.db.get_heroes()
            
            # Choose a random hero and also set the class
            self.set_hero(random.choice(valid_heroes))

        # Set cards
        valid_cards = self.db.get_cards(class_name=self.hero_class) + self.db.get_cards(class_name="Neutral")
        while len(self.cards) < card_count:
            # Choose a random card
            random_card = random.choice(valid_cards)

            # TODO? Implement card limit based on the rarity of the card
            self.cards.append(random_card)

    def generate_deck_from_text_file(self, textfile):
        """
        Fill out the deck from the content of the given text file.

        Parameters
        ----------
        textfile : str
            Path to the .txt file
        """

        try:
            with open(textfile, "r") as f:
                # Read deck name
                line = f.readline()
                deck_name = " ".join(line.split()[1:])

                # Read class name
                line = f.readline()
                class_name = " ".join(line.split()[1:])

                # Read hero name
                line = f.readline()
                hero_name = " ".join(line.split()[1:])

                if self.db.check_hero(hero_name) == False:
                    print("Invalid hero:", hero_name)
                    return False

                hero_class = self.db.get_hero_class(hero_name)
                if hero_class.lower() != class_name.lower():
                    print("Invalid class:", class_name)
                    return False

                # Read cards
                card_names = []
                for line in f:
                    card_name = line.strip()
                    if self.db.check_card(card_name) == False:
                        print("Invalid card:", card_name)
                        return False
                    elif self.db.check_neutral(card_name) == False and self.db.check_card_class(card_name, hero_class) == False:
                        print("Invalid card (wrong class):", card_name)
                        return False
                    card_names.append(card_name)

                if len(card_names) > 30:
                    print("Too many cards in deck")
                    return False

                # TODO? Implement card limit based on the rarity of the card

                # Everything is valid, replace deck information
                self.name = deck_name
                self.hero = hero_name
                self.hero_class = hero_class
                self.cards = card_names

                return True
        except:
            print("Error while reading text file")
            return False

    def __str__(self):
        """
        Conversion to string, e.g. when the print() function is called
        """

        deck_str = ""

        # Deck name
        if self.name is not None:
            deck_str += self.name + "\n"
        else:
            deck_str += "Unnamed Deck\n"

        # Hero and class
        if self.hero is not None:
            deck_str += "Hero: {} ({})\n".format(self.hero, self.hero_class)
        else:
            deck_str += "Hero: Unknown\n"

        # Cards
        deck_str += "Cards:\n"
        for card in self.cards:
            deck_str += card + "\n"

        return deck_str
