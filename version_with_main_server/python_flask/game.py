# dict: key - login user is create lobby, value - name game
game_lobbies = dict()

def create_lobby(login_user: str, name_game: str):
    '''create lobby of user'''
    game_lobbies.setdefault(login_user, name_game)

def is_lobby(login_user: str, name_game: str) -> bool:
    '''return bool contains game lobby with this user'''
    return login_user in game_lobbies and game_lobbies[login_user] == name_game

def remove_lobby(login_user: str):
    del game_lobbies[login_user]
