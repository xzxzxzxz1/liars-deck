from models.guest import Guest
from models.game import Game
class Lobby:
    def __init__(self):
        self.guests = []   # List of players in the lobby
        self.game = None
        self.games = []     # List of completed games
        
    def add_guest(self, guest):
        # Adds a new player to the lobby
        if len(self.guests) == 4:
            print("Maximum Lobby Size. Cannot add anymore players.")
            return False
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
            
        g = Game(self.guests)
        winner = g.get_winner()
        self.increment_win(winner)
        return True 
    
    def view_lobby(self):
        print("______LOBBY_______")
        for guest in self.guests:
            print(f"{guest.name}: {guest.wins} wins\n")
        print("__________________")
        
    def increment_win(self, player_name):
        for guest in self.guests:
            if player_name == guest.name:
                guest.wins += 1
            else:
                guest.losses += 1