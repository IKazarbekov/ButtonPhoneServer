# set tuples: login_one, login_two, map(str with length 9), step_first_player: bool
# login_one - X player, login_two - O player

games = set()

def create_game(login_one, login_two):
    """create game"""
    games.add((login_one, login_two, '123456789', True))

def get_map(login: str) -> str:
    """getter game_map str"""
    for game in games:
        log_1, log_2, game_map, _ = game
        if log_1 == login or log_2 == login:
            return processing_map_to_html(game_map)

def is_in_game(login: str) -> bool:
    """return getter is_in_game"""
    for game in games:
        log_1, log_2, game_map, _ = game
        if log_1 == login or log_2 == login:
            return True
    return False

def get_enemy(login: str) -> str:
    """return getter is_in_game"""
    for game in games:
        log_1, log_2, game_map, _ = game
        if log_1 == login:
            return log_2
        if log_2 == login:
            return log_1

def processing_map_to_html(game_map: str) -> str:
    """transform from str to html"""
    result_html = "<h1>"
    for y in range(3):
        for x in range(3):
            char = game_map[y * 3 + x]
            result_html += char + " "
        result_html += '<br/>'
    result_html += "<h1/>"
    return result_html

def went(login: str, step: str):
    """user create step"""
    try:
        log1, log2, game_map, step_first_player = __find_game__(login)
        int_step = int(step) - 1

        if not game_map[int_step].isdigit():       # if area not clear
            return
        games.remove((log1, log2, game_map, step_first_player)) # remove old data
        step_first_player = not step_first_player   # invert step
        if log1 == login:
            game_map = game_map[0:int_step] + 'X' + game_map[int_step+1:]
        else:
            game_map = game_map[0:int_step] + 'O' + game_map[int_step+1:]
        games.add((log1, log2, game_map, step_first_player))    # append new data
    except IndexError as e:
        """None action after exception"""
        pass
    except ValueError as e:
        pass

def is_step(login: str):
    """player went ?"""
    log1, log2, game_map, is_step_first_player = __find_game__(login)
    if log1 == login:
        return is_step_first_player
    else:
        return not is_step_first_player

def who_winner(login: str) -> str:
    """
    for win game
    if game continue, then return None
    :param login: user login
    :return: who is the winner in great str
    """
    log1, log2, game_map, is_step_first_player = __find_game__(login)

    for i in range(3):
        I = i * 3
        if game_map[I] == game_map[I + 1] == game_map[I + 2]: # rows
            return f"Выиграл {game_map[I]} !"
        if game_map[i] == game_map[3 + i] == game_map[6 + i]: # columns
            return f"Выиграл {game_map[i]} !"

    if game_map[0] == game_map[4] == game_map[8]: # main diagonal
        return f"Выиграл {game_map[0]} !"
    if game_map[2] == game_map[4] == game_map[6]: # side diagonal
        return f"Выиграл {game_map[2]} !"

    if all(not char.isdigit() for char in game_map):
        return "Ничья !"

    return None

def __find_game__(login: str):
    """find game by login user"""
    for game in games:
        log_1, log_2, map, _ = game
        if log_1 == login or log_2 == login:
            return game