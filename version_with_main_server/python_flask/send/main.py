from flask import Flask, redirect, request
import chat, game
from front import page
import session
import tictactoe

# application Flask
application = Flask(__name__)
app = application

# root
@app.route('/')
def root():
    return redirect('/login')

# page login
@app.route('/login')
def login():
    args = request.args
    ip = request.remote_addr

    if session.contains(ip):
        return redirect('/main_menu')
    return page.LOGIN

@app.route('/login/guest')
def log_guest():
    args = request.args
    ip = request.remote_addr

    if 'log' in args:
        if 'kno' in args:
            session.add_guest(ip, args['log'], True)
        else:
            session.add_guest(ip, args['log'], False)
        return redirect('/main_menu')
    else:
        return redirect('/login')

@app.route('/login/exit')
def log_exit():
    args = request.args
    ip = request.remote_addr

    if session.contains(ip):
        session.remove(ip)
    return redirect("/login")


# main menu
@app.route('/main_menu')
def main_menu():
    args = request.args
    ip = request.remote_addr
    if not session.contains(ip):
        return redirect('/login')
    login, button_phone = session.get_log_and_but(ip)

    return page.main_menu(login, button_phone)

# chat
@app.route('/chat')
def rchat():
    args = request.args
    ip = request.remote_addr
    if not session.contains(ip):
        return redirect('/login')
    login = session.get_login(ip)

    if 'mes' in args:
        chat.add_message(login, args['mes'])
        return redirect('/chat')

    text_messages = chat.get_all_messages()
    return page.chat(text_messages)

# tic tac toe
@app.route('/ttt')
def ttt():
    args = request.args
    ip = request.remote_addr
    if not session.contains(ip):
        return redirect('/login')
    login = session.get_login(ip)

    return page.tictactoe_menu()

# tic tac toe game
@app.route('/ttt/game')
def ttt_game():
    args = request.args
    ip = request.remote_addr
    if not session.contains(ip):
        return redirect('/login')
    login = session.get_login(ip)


    # if arg log contains, then this user join in game
    if 'log' in args:
        login_to_user = args['log']
        if game.is_lobby(login_to_user, 'tic-tac-toe'):
            game.remove_lobby(login_to_user,)
            tictactoe.create_game(login, login_to_user)

            game_map = tictactoe.get_map(login)
            is_step = tictactoe.is_step(login)
            return redirect('/ttt/game')
        else:
            return page.error_join_game()

    # if user in game
    if tictactoe.is_in_game(login):
        # if user went
        if 'step' in args:
            step = args['step']
            tictactoe.went(login, step)
            return redirect('/ttt/game')

        # if there is a winner
        winner = tictactoe.who_winner(login)
        if not winner is None:
            return page.winner_game(winner)

        game_map = tictactoe.get_map(login)
        log_enemy = tictactoe.get_enemy(login)
        is_step = tictactoe.is_step(login)
        return page.tictactoe_game(log_enemy, game_map, is_step)

    # if args not, then user create lobby
    game.create_lobby(login, 'tic-tac-toe')

    return page.tictactoe_wait(login)

@app.route('/game/exit')
def exit_game():
    pass

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5001)