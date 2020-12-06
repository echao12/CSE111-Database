import os
from Deck import Deck

class App:
    """
    A class used to represent the application.

    Attributes
    ----------
    db : HSDB
        A reference to the Hearthstone database
    decks : list of Deck objects
        A list of decks stored in the application
    """

    def __init__(self, db):
        """
        Constructor
        """

        self.db = db
        self.decks = []

    def run(self):
        """
        Start the main loop of the application. 
        """

        running = True
        while running:
            # Display the available commands
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Welcome to the Hearthstone database app!")
            print("[1] View decks")
            print("[2] Create new deck")
            print("[3] Edit existing deck")
            print("[4] Delete deck")
            print("[5] Create deck from text file")
            print("[6] Save deck to file")
            print("[7] Create random deck")
            print("[8] Search for cards")
            print("[0] Exit the application")
            print("")

            # Ask for input
            key = input("Please select your action: ")
            key = key.strip().lower()
            print("")
            
            # Convert the input to integer
            valid_key = True
            try:
                key = int(key)
            except:
                valid_key = False

            # Decide what to run based on the input
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
                self.save_deck_to_file()
            
            elif key == 7:
                self.create_random_deck()
            
            elif key == 8:
                self.search_cards()
            
            elif key == 0:
                print("Exiting application...")
                running = False
            
            else:
                print("Invalid input")

            # Pause the application until the Enter key is pressed
            input("\nPress Enter to continue...")

    def check_duplicate_name(self, name):
        """
        Check if there is already a deck with the given name.

        Parameters
        ----------
        name : str
            The name to be checked
        """

        is_duplicate = False
        for deck in self.decks:
            if name == deck.name:
                is_duplicate = True

        return is_duplicate

    def view_decks(self):
        """
        Enter the part of the application where the user can view the list of decks stored in the application.
        """

        if len(self.decks) == 0:
            print("There is no deck yet")
        else:
            # Display the available decks
            print("You currently have the following decks: ")
            for deck in self.decks:
                print(deck.name)
            print("")

            # An optional request to look at a particular deck in more detail
            deck_name = input("Enter the name of the deck you want to view, or skip to go back: ")
            deck_name = deck_name.strip()
            print("")

            if deck_name == "":
                return
            else:
                for deck in self.decks:
                    if deck_name == deck.name:
                        print(deck)  # Print the content of the deck
                        deck.print_deck_statistics()  # Print the statistics
                        return

    def create_deck(self):
        """
        Enter the part of the application where the user can create a new deck manually.
        """

        # Ask for the name of the deck to be created
        deck_name = input("Please enter the name of your new deck: ")
        deck_name = deck_name.strip()
        print("")

        # Check if the name is already taken
        if self.check_duplicate_name(deck_name) == True:
            print("Deck name is already taken")
            return

        # Ask for the name of the hero
        hero_name = input("Please enter the name of your hero: ")
        hero_name = hero_name.strip()
        print("")

        # Check if it is a valid hero
        if self.db.check_hero(hero_name) == False:
            print("Invalid hero")
            return

        # Create the deck (no cards yet)
        new_deck = Deck(self.db, deck_name, hero_name)

        # Ask for the first card
        card_name = input("Pick a card: ")
        card_name = card_name.strip()
        print("")

        entering_cards = True
        while entering_cards:
            # Try adding the card to the deck
            if new_deck.add_card(card_name) == True:
                print("Card successfully added to the deck\n")
            else:
                print("Failed to insert card\n")

            # Ask for another card
            card_name = input("Pick another card (type 'done' when you're finished): ")
            card_name = card_name.strip()
            print("")

            # A way to exit the loop gracefully
            if card_name == "done":
                entering_cards = False

        # Append the newly created deck to the list
        self.decks.append(new_deck)        

    def edit_deck(self):
        """
        Enter the part of the application where the user can edit an existing deck.
        """

        # Ask for the name of the deck to be edited
        deck_name = input("Please enter the name of the deck you want to edit: ")
        deck_name = deck_name.strip()
        print("")

        # Get reference to the deck
        deck = None
        for d in self.decks:
            if deck_name == d.name:
                deck = d

        # Check if the deck exists
        if deck is None:
            print("Deck does not exist")
            return

        # Enter the editing loop
        editing = True
        while editing:
            # Display the available commands
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Editing", deck.name)
            print("[1] Change deck name")
            print("[2] Add card")
            print("[3] Remove card")
            print("[4] View cards")
            print("[0] Return to main menu")
            print("")

            # Ask for input
            key = input("Please select your action: ")
            key = key.strip().lower()
            print("")

            # Convert input to integer            
            valid_key = True
            try:
                key = int(key)
            except:
                valid_key = False

            # Decide what to do based on the input
            if valid_key == False:
                print("Invalid input")

            elif key == 1:  # Change deck name
                # Ask for the new name
                new_name = input("Please enter the new deck name: ")
                new_name = new_name.strip()
                print("")

                # Check if the name is already taken
                if self.check_duplicate_name(new_name) == True:
                    print("That name is already taken")
                else:
                    # Set new name
                    deck.set_name(new_name)
                    print("Deck name has been changed to", deck.name)

            elif key == 2:  # Add a card
                # Ask for the card name
                card_name = input("Please enter the name of the card: ")
                card_name = card_name.strip()
                print("")

                # Try adding the card to the deck
                if deck.add_card(card_name) == True:
                    print("Card successfully added to the deck")
                else:
                    print("Failed to insert card")

            elif key == 3:  # Remove a card
                # Ask for the card name
                card_name = input("Please enter the name of the card: ")
                card_name = card_name.strip()
                print("")

                # Check if the card is in the deck. If so, remove it.
                if deck.check_card(card_name) == True:
                    deck.remove_card(card_name)
                    print("Card successfully removed from the deck")
                else:
                    print("Unable to find card in deck")

            elif key == 4:  # View all the cards currently in the deck
                print("This deck currently has", len(deck.cards), "cards")
                for card in deck.cards:
                    print(card)

            elif key == 0:  # Exit the loop gracefully
                editing = False

            else:
                print("Invalid input")

            input("\nPress Enter to continue...")        

    def delete_deck(self):
        """
        Enter the part of the application where the user can delete an existing deck.
        """

        # Ask for the name of the deck
        deck_name = input("Please enter the name of the deck you want to delete: ")
        deck_name = deck_name.strip()
        print("")

        # Find the deck and delete it if it exists
        for deck in self.decks:
            if deck_name == deck.name:
                self.decks.remove(deck)
                del deck
                print(deck_name, "is successfully deleted")
                return

        print("Deck not found")

    def create_deck_from_txt(self):
        """
        Enter the part of the application where the user can create a deck from a text file.
        """

        # Ask for the name of the txt file
        file_name = input("Enter the name of the text file: ")
        file_name = file_name.strip()
        print("")

        # Check if it is a valid text file
        if not os.path.isfile(file_name):
            print("Error: Either input is not a file, or the file does not exist")
        elif file_name[-4:] != ".txt":
            print("Error: The given file must be a .txt file")
        else:
            # Attempt to generate a new deck using the text file
            new_deck = Deck(self.db)
            success = new_deck.generate_deck_from_text_file(file_name)

            if success:
                # Check if the deck's name is already taken
                if self.check_duplicate_name(new_deck.name):
                    print("Failed to create deck: the deck name is already taken")
                else:
                    # Append the deck to the list
                    self.decks.append(new_deck)
                    print("Deck successfully created")
                    print("")

                    # Print it too so the user knows what's in the deck
                    print(new_deck)
            else:
                print("Failed to create deck")

    def save_deck_to_file(self):
        """
        Enter the part of the application where the user can save a deck to a file.
        """

        # Ask for the name of the deck
        deck_name = input("Please enter the name of the deck you want to save: ")
        deck_name = deck_name.strip()
        print("")

        # Search for the deck in the list
        for deck in self.decks:
            if deck_name == deck.name:
                # Can't save a deck that doesn't yet have a hero or a single card
                if deck.hero is None or len(deck.cards) == 0:
                    print("Deck is incomplete")
                    return

                # Ask for the name of the save file
                file_name = input("Enter the name of the file (recommended to use .txt): ")
                file_name = file_name.strip()
                print("")

                # Check if that file already exists
                if os.path.isfile(file_name):
                    # If yes, ask the user if it's ok to overwrite it
                    ok = input("File already exists. Overwrite (yes/no)? ")
                    ok = ok.strip().lower()
                    print("")

                    if ok != "yes" and ok != "y" and ok != "ok":
                        print("Returning to main menu")
                        return

                # Attempt to save the deck to the file
                try:
                    with open(file_name, 'w') as f:
                        f.write("Name {}\n".format(deck.name))
                        f.write("Class {}\n".format(deck.hero_class))
                        f.write("Hero {}\n".format(deck.hero))
                        for card in deck.cards:
                            f.write(card + "\n")

                        print(deck_name, "is successfully saved to", file_name)
                except:
                    print("Error: Unable to save deck to", file_name)
                
                return

        # This point is only reached if the requested deck does not exist in the list
        print("Deck not found")

    def create_random_deck(self):
        """
        Enter the part of the application where the user can create a random deck automatically.
        """

        # Create an empty deck
        new_deck = Deck(self.db)

        accept = False
        while not accept:
            # Clear the screen for better visibility
            os.system('cls' if os.name == 'nt' else 'clear')

            # Randomize the deck and display it
            new_deck.randomize()
            print(new_deck)

            # Ask if the user wants to save this deck
            ok = input("Create this deck (yes/no/cancel)? ")
            ok = ok.strip().lower()

            if ok == "yes" or ok == "y" or ok == "ok":
                # Check if the randomly generated name has already been taken (should be highly unlikely)
                if self.check_duplicate_name(new_deck.name):
                    print("Failed to create deck: the deck name is already taken")
                else:
                    # Append the deck to the list
                    accept = True
                    self.decks.append(new_deck)
                    print("Deck successfully created")

            elif ok == "no" or ok == "n":
                # Continue the loop
                continue

            elif ok == "cancel" or ok == "c":
                # Exit the loop gracefully
                accept = True

            else:
                # Exit the loop less gracefully
                accept = True
                print("Invalid input")
    
    def search_cards(self):
        """
        Enter the part of the application where the user can search for cards in the database.
        """

        # Ask for the card name search parameter
        card_name = input("Enter full/partial card name (press Enter to skip): ")
        card_name = card_name.strip()
        print("")

        if card_name == "":
            card_name = None

        # Ask for the card cost search parameter
        card_cost = input("Enter mana cost (press Enter to skip): ")
        card_cost = card_cost.strip()
        print("")

        if card_cost == "":
            card_cost = None
        else:
            try:
                # Convert to integer
                card_cost = int(card_cost)
            except:
                print("Invalid card cost")
                return

        # Ask for the card rarity search parameter
        card_rarity = input("Enter card rarity (Free/Common/Rare/Epic/Legendary) (press Enter to skip): ")
        card_rarity = card_rarity.strip().lower()
        print("")

        if card_rarity == "":
            card_rarity = None
        elif card_rarity != "free" and card_rarity != "common" and card_rarity != "rare" and card_rarity != "epic" and card_rarity != "legendary":
            print("Invalid card rarity")
            return

        # Ask for the card type search parameter
        card_type = input("Enter card type (Minion/Spell/Weapon) (press Enter to skip): ")
        card_type = card_type.strip().lower()
        print("")

        if card_type == "":
            card_type = None
        elif card_type != "minion" and card_type != "spell" and card_type != "weapon":
            print("Invalid card type")
            return

        # Ask for the class name search parameter
        class_name = input("Enter full class name (press Enter to skip): ")
        class_name = class_name.strip()
        print("")

        if class_name == "":
            class_name = None
        elif self.db.check_class(class_name) == False:
            print("Invalid class name")
            return

        # Query the database for all the cards matching the parameters
        search_results = self.db.get_cards(card_name, card_cost, card_rarity, card_type, class_name)

        # Display a summary of the search parameters
        print("Search parameters:")
        print("Card Name:", card_name if card_name is not None else "None")
        print("Mana Cost:", card_cost if card_cost is not None else "None")
        print("Card Rarity:", card_rarity if card_rarity is not None else "None")
        print("Card Type:", card_type if card_type is not None else "None")
        print("Class Name:", class_name if class_name is not None else "None")
        print("")
        
        # Display the search results
        if len(search_results) == 0:
            print("No results found")
        else:
            print(len(search_results), "cards found")
            for card in search_results:
                print(card)
