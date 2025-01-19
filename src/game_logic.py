import random
from player import Player

class Guest:
    def __init__(self, display_name):
        self.name = display_name
        self.is_ready = False
        self.wins = 0
        self.losses = 0
        
    def toggle_ready(self):
        # Have a button for each guest that 
        # they can press to toggle their ready status
        self.is_ready = not self.is_ready
        return self.is_ready
    
    def increment_win(self):
        self.wins += 1
    
    def increment_loss(self):
        self.losses += 1

    def __repr__(self):
        return f"Guest(display_name={self.name}, is_ready={self.is_ready})"
        
class Lobby:
    def __init__(self):
        self.guests = []   # List of players in the lobby
        self.game = None
        self.games = []     # List of completed games
        
    def add_guest(self, guest):
        # Adds a new player to the lobby
        if guest in self.guests:
            print("ERROR: Name already taken. Please try a new name")
            return False
        self.guests.append(guest)
        print("{guest} has joined the lobby.".format(guest = guest.name))
    
    def remove_guest(self, guest):
        # Player removed by the lobby creator
        # Might need case where they can't remove themselves otherwise that will cause error
        if guest in self.guests:
            self.guests.remove(guest)
            print("{guest} has been removed from the lobby.".format(guest = guest.name))
        else:
            print("ERROR: Guest to remove doesn't exist")
    
    def guest_leave(self, guest):
        # Guests leaving on their own accord
        if guest in self.guests:
            self.guests.remove(guest)
            print("{guest} has left the lobby.".format(guest = guest.name))
        else:
            print("ERROR: Leaving guest doesn't exist")
        
    def all_ready(self):
        for guest in self.guests:
            if guest.is_ready == False:
                return False
        return True
    
    def start_game(self):
        if not self.all_ready():
            print("Not all guests are ready. Cannot start the game.")
            return False
        
        if len(self.guests) <= 1:
            print("Cannot start game with just one player.")
            return False
            
        self.game = Game(self.guests)
        return True 
    
class Game:
    def __init__(self, guests):
        self.players = [Player(guest) for guest in guests]
        self.num_players = len(self.players)
        self.ongoing = True
        self.winner = None
        
    def play_game(self):
        while self.ongoing == True:
            # Keeps track of the round and also continues initiating Round class as long 
            # as game status is True / Ongoing
            Round(self.players)
            self.status_update
        # Once game status toggles to false we will close the game and 
        # award victory to the last remaining player
        self.winner = self.players[0]
        return self.winner
    
    def status_update(self):
        self.players = [player for player in self.players if player.alive]
        self.num_players = len(self.players)
        if self.num_players == 1:
            self.ongoing = False
        return True

class Round:
    def __init__(self, players):
        self.players = players
        self.ongoing = True
        self.playcard = self.initialise_playcard()
        self.initialise_hands()
        self.previous_hand = None
        self.previous_player = None

    def play_round(self):
        while self.ongoing == True:
            for player in self.players:
                current_turn = Turn(player)
                if current_turn == 'B':
                    self.call_bluff(player, self.previous_player)
                else: 
                    amount = len(current_turn)
                    print(f"{player}: {amount} {self.playcard}!")
                    self.previous_hand = current_turn
                    self.previous_player = player
        return True
        
    def initialise_playcard(self):
        draw = ['A', 'K', 'Q']
        round_card = random.choice(draw)
        if round_card == 'A':
            round_card_print = 'Ace'
        elif round_card == 'K':
            round_card_print = 'King'
        elif round_card == 'Q':
            round_card_print = 'Queen'
        
        print(f"{round_card_print}'s Table!")
        
        return round_card
        
    def start_turn_timer(self):
        # 30 second timer 
        self.end_turn()
        pass

    def initialise_hands(self):
        # Randomly distributes 5 cards to each of the players from a deck of
        # 6 Kings, 6 Aces, 6 Queens, 2 Jokers
        deck = ['A'] * 6 + ['K'] * 6 + ['Q'] * 6 + ['J'] * 2
        random.shuffle(deck)
        
        for player in self.players:
            player.hand = [deck.pop() for _ in range(5)]

        print("There are 6 Aces, 6 Kings, 6 Queens and 2 Jokers in the deck.")
    
    def roulette(self, player):
        bullet_chamber = random.randint(1, player.max_lives)
        shot = random.randint(1, player.max_lives)
        print("Waiting...")
        # Make a 3 second wait timer
        
        if shot == bullet_chamber:
            print("The chamber contained a bullet!")
            player.eliminate()
        else:
            print("The chamber was empty! " + player.name + " lives another day!")
            player.max_lives -= 1
        
        self.ongoing = False   
    
    def call_bluff(self, current_player, previous_player):
        print("Liar!")
        correct_hands = self.generate_valid_hands(self.playcard, len(self.previous_hand))
        
        if self.previous_hand in correct_hands:
            current_player.roulette()
            return False # Incorrect bluff call
        
        previous_player.roulette()
        return True # Correct bluff call, previous hand was a bluff!
            
    def generate_valid_hands(self, playcard, hand_size):
        from itertools import product
        
        possible_cards = [playcard, 'J']
        
        valid_hands = product(possible_cards, hand_size)
        
        return [list(hand) for hand in valid_hands]
        
class Turn:
    def __init__(self, player):
        self.player = player
        self.print_instructions()
        self.get_action()

    def print_instructions(self):
        if self.player.instructions == True:
            print(f"CURRENT PLAYER: {self.player.display_name()}")
            print("It is now your turn!")
            print("Enter B to call Bluff.")
            print("Enter the index 1 - 5 of the cards you want to play separated by just a comma")
            print("For example if your hand is [K, K, Q, J, Q] you may enter '1,2' to play two cards which are") 
            print("your first and second cards which both Kings or something like'3' to play your 3rd card (Queen)")
            print("Enter I to toggle the instruction display.")
        
        print("Your hand is currently:" + self.player.hand)
    
    def get_action(self):
        while True:
            user_input = input("Enter your action: ").upper()
            
            if user_input == 'B':
                return user_input
                # Call Bluff
            elif user_input == 'I':
                self.player.instructions = not self.player.instructions
                state = "on" if self.player.instructions else "off"
                print(f"Instructions are now turned {state}.")
                continue
            
            else: 
                try: 
                    inputs = [int(i) for i in user_input.split(",")]
                except ValueError:
                    print("ERROR: Please enter valid integers separated by commas.")
                    continue
                
                if self.validate_indices(inputs):
                    play_cards = [self.player.hand[i - 1] for i in inputs]
                    return play_cards
                else: 
                    continue
    
    def validate_indices(self, indices):
        if any(i < 0 or i > len(self.player.hand) for i in indices):
            print("ERROR: Index out of the range of the player's hand!")
            return False
        if len(set(indices) != len(indices)):
            print("ERROR: Please do not play duplicate indices")
            return False
        
        return True
            