import os
from Deck import Deck

class App:
    """
    TODO: Documentation
    TODO: Formatting
    TODO: Helpful comments
    """

    def __init__(self, db):
        self.db = db
        self.decks = []

    def run(self):
        running = True
        while running:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Welcome to the Hearthstone database app!")
            print("[1] View decks")
            print("[2] Create new deck")
            print("[3] Edit existing deck")
            print("[4] Delete deck")
            print("[5] Create deck from text file")
            print("[6] Create random deck")
            print("[7] Search for cards")
            print("[0] Exit the application")
            print("")
            key = input("Please select your action: ")
            key = key.strip().lower()
            print("")
            
            valid_key = True
            try:
                key = int(key)
            except:
                valid_key = False

            if valid_key == False:
                print("Invalid input")
            elif key == 1:
                self.view_decks()
            elif key == 2:
                self.create_deck()
            elif key == 3:
                self.edit_deck()
            elif key == 4:
                self.delete_deck()
            elif key == 5:
                self.create_deck_from_txt()
            elif key == 6:
                self.create_random_deck()
            elif key == 7:
                self.search_cards()
            elif key == 0:
                print("Exiting application...")
                running = False
            else:
                print("Invalid input")

            input("\nPress Enter to continue...")

    def check_duplicate_name(self, name):
        is_duplicate = False
        for deck in self.decks:
            if name == deck.name:
                is_duplicate = True
        return is_duplicate

    def view_decks(self):
        if len(self.decks) == 0:
            print("There is no deck yet")
        else:
            print("You currently have the following decks: ")
            for deck in self.decks:
                print(deck.name)

            print("")
            deckname = input("Enter the name of the deck you want to view, or skip to go back: ")
            deckname = deckname.strip()
            print("")

            if deckname == "":
                return
            else:
                deck_match = False
                for deck in self.decks:
                    if deckname == deck.name:
                        deck_match = True
                        print(deck)
                        deck.print_deck_statistics()

                if deck_match == False:
                    print("There is no deck with the given name")

    def create_deck(self):
        deck_name = input("Please enter the name of your deck: ")
        deck_name = deck_name.strip()
        print("")

        if self.check_duplicate_name(deck_name) == True:
            print("Deck name is already taken")
            return

        hero_name = input("Please enter the name of your hero: ")
        hero_name = hero_name.strip()
        print("")

        if self.db.check_hero(hero_name) == False:
            print("Invalid hero")
            return

        new_deck = Deck(self.db, deck_name, hero_name)

        card_name = input("Pick a card: ")
        card_name = card_name.strip()
        print("")

        entering_cards = True
        while entering_cards:
            if new_deck.add_card(card_name) == True:
                print("Card successfully added to the deck\n")
            else:
                print("Failed to insert card\n")

            card_name = input("Pick another card (type 'done' when you're finished): ")
            card_name = card_name.strip()
            print("")

            if card_name == "done":
                entering_cards = False

        self.decks.append(new_deck)        

    def edit_deck(self):
        deck_name = input("Please enter the name of the deck you want to edit: ")
        deck_name = deck_name.strip()
        print("")

        deck = None
        for d in self.decks:
            if deck_name == d.name:
                deck = d

        if deck is None:
            print("Deck does not exist")
            return

        editing = True
        while editing:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Editing", deck.name)
            print("[1] Change deck name")
            print("[2] Add card")
            print("[3] Delete card")
            print("[4] View cards")
            print("[0] Return to main menu")
            print("")
            key = input("Please select your action: ")
            key = key.strip().lower()
            print("")
            
            valid_key = True
            try:
                key = int(key)
            except:
                valid_key = False

            if valid_key == False:
                print("Invalid input")

            elif key == 1:
                new_name = input("Please enter the new deck name: ")
                new_name = new_name.strip()
                print("")

                if self.check_duplicate_name(new_name) == True:
                    print("That name is already taken")
                else:
                    deck.set_name(new_name)
                    print("Deck name has been changed to", deck.name)

            elif key == 2:
                card_name = input("Please enter the name of the card: ")
                card_name = card_name.strip()
                print("")

                if deck.add_card(card_name) == True:
                    print("Card successfully added to the deck")
                else:
                    print("Failed to insert card")

            elif key == 3:
                card_name = input("Please enter the name of the card: ")
                card_name = card_name.strip()
                print("")

                if deck.check_card(card_name) == True:
                    deck.remove_card(card_name)
                    print("Card successfully removed from the deck")
                else:
                    print("Unable to find card in deck")

            elif key == 4:
                for card in deck.cards:
                    print(card)

            elif key == 0:
                editing = False

            else:
                print("Invalid input")

            input("\nPress Enter to continue...")        

    def delete_deck(self):
        deck_name = input("Please enter the name of the deck you want to delete: ")
        deck_name = deck_name.strip()
        print("")

        for deck in self.decks:
            if deck_name == deck.name:
                self.decks.remove(deck)
                del deck
                print(deck_name, "is successfully deleted")
                return

        print("Deck not found")

    def create_deck_from_txt(self):
        filename = input("Enter the name of the textfile: ")
        filename = filename.strip()
        print("")

        if not os.path.isfile(filename):
            print("Error: Either input is not a file, or the file does not exist")
        elif filename[-4:] != ".txt":
            print("Error: The given file must be a .txt file")
        else:
            new_deck = Deck(self.db)
            success = new_deck.generate_deck_from_text_file(filename)

            if success:
                if self.check_duplicate_name(new_deck.name):
                    print("Failed to create deck: the deck name is already taken")
                else:
                    self.decks.append(new_deck)
                    print("Deck successfully created")
                    print("")
                    print(new_deck)
            else:
                print("Failed to create deck")

    def create_random_deck(self):
        new_deck = Deck(self.db)
        accept = False
        while not accept:
            os.system('cls' if os.name == 'nt' else 'clear')

            new_deck.randomize()
            print(new_deck)

            ok = input("Create this deck (yes/no/cancel)? ")
            ok = ok.strip().lower()

            if ok == "yes" or ok == "y" or ok == "ok":
                if self.check_duplicate_name(new_deck.name):
                    print("Failed to create deck: the deck name is already taken")
                else:
                    accept = True
                    self.decks.append(new_deck)
                    print("Deck successfully created")
            elif ok == "no" or ok == "n":
                continue
            elif ok == "cancel" or ok == "c":
                accept = True
            else:
                accept = True
                print("Invalid input")
    
    def search_cards(self):
        card_name = input("Enter full/partial card name (press Enter to skip): ")
        card_name = card_name.strip()
        print("")

        if card_name == "":
            card_name = None

        card_cost = input("Enter mana cost (press Enter to skip): ")
        card_cost = card_cost.strip()
        print("")

        if card_cost == "":
            card_cost = None
        else:
            try:
                card_cost = int(card_cost)
            except:
                print("Invalid card cost")
                return

        card_rarity = input("Enter card rarity (Free/Common/Rare/Epic/Legendary) (press Enter to skip): ")
        card_rarity = card_rarity.strip().lower()
        print("")

        if card_rarity == "":
            card_rarity = None
        elif card_rarity != "free" and card_rarity != "common" and card_rarity != "rare" and card_rarity != "epic" and card_rarity != "legendary":
            print("Invalid card rarity")
            return

        card_type = input("Enter card type (Minion/Spell/Weapon) (press Enter to skip): ")
        card_type = card_type.strip().lower()
        print("")

        if card_type == "":
            card_type = None
        elif card_type != "minion" and card_type != "spell" and card_type != "weapon":
            print("Invalid card type")
            return

        class_name = input("Enter full class name (press Enter to skip): ")
        class_name = class_name.strip()
        print("")

        if class_name == "":
            class_name = None
        elif self.db.check_class(class_name) == False:
            print("Invalid class name")
            return

        search_results = self.db.get_cards(card_name, card_cost, card_rarity, card_type, class_name)

        print("Search parameters:")
        print("Card Name:", card_name if card_name is not None else "None")
        print("Mana Cost:", card_cost if card_cost is not None else "None")
        print("Card Rarity:", card_rarity if card_rarity is not None else "None")
        print("Card Type:", card_type if card_type is not None else "None")
        print("Class Name:", class_name if class_name is not None else "None")
        print("")
        
        if len(search_results) == 0:
            print("No results found")
        else:
            print(len(search_results), "cards found")
            for card in search_results:
                print(card)
