
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
        self.players.append(guest)
        print("{guest} has joined the lobby.".format(guest = guest.name))
    
    def remove_guest(self, guest):
        # Player removed by the lobby creator
        # Might need case where they can't remove themselves otherwise that will cause error
        if guest in self.guests:
            self.players.remove(guest)
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
        self.rounds = []
        self.ongoing = True
        
        def play_game(self):
            while self.ongoing == True:
                # Keeps track of the round and also continues initiating Round class as long 
                # as game status is True / Ongoing
                self.rounds.append(Round(self.players))
                
            # Once game status toggles to false we will close the game and 
            # award victory to the last remaining player
            return False
            # Should exit game here?
        
        def exit_game(self):
            # How do i even code this?
        
class Round:
    def __init__(self, players):
        pass
        
    def initialise_hands(self, players):
        # Randomly distributes 5 cards to each of the players from a deck of
        # 6 Kings, 6 Aces, 6 Queens, 2 Jokers
        pass
    
    def play_round(self):
        pass
        
    def start_turn_timer(self):
        # 30 second timer 
        self.end_turn()
        pass

    def end_turn(self):
        pass
    

class Turn:
    pass