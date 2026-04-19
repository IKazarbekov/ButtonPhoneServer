from front import page_builder as pb

LOGIN = pb.create_page([
    pb.Card("KnoTl", [
        [
            pb.Label("Сайт для кнопочных телефонов"),
            pb.Label("Введите любой логин"),
            pb.Form([
                pb.TextBox("логин", "log"),
                pb.CheckBox("Кнопочный телефон", "kno")
            ], url='/login/guest')
        ]
    ])
],
False)

def main_menu(login: str, button_phone: bool = False):
    return pb.create_page([
        pb.Card("KnoTl", [
            [
                pb.Label(f"Добро пожаловать: {login}"),
            ],
            [
                pb.Url("Чат", "/chat"),
            ],
            [
                pb.Url("Крестики-Нолики", "/ttt"),
            ],
            [
                pb.Url("О сайте", "#a"),
            ],
            [
                pb.Url("выйти из сессии", "/login/exit"),
            ]
        ], id="m"),
        pb.Card("О сайте", [
            pb.Label(f"Сайт для кнопочных телефонов, использует формат wml html, все скрипты происходят на сервере. Наслаждайтесь !"),
            pb.Label(f"Версия: 0.2"),
            pb.Url("В меню", "#m"),
        ], id="a"),
    ], button_phone)

def chat(messages: str, is_button_phone: bool = False) -> str:
    if is_button_phone:
        return f"""<?xml version="1.0"?>
<!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN" "http://www.wapforum.org/DTD/wml_1.1.xml">
<wml>

<card id="chat" title="Чат" ontimer="">
    <timer value="50"/>  <!-- 5 секунд (в 0.1 секунды = 50 = 5 сек) -->
    
    <p align="center">
        <strong>Чат</strong><br/>
        <br/>
        ---------------------------------<br/>
        {messages}
        ---------------------------------<br/>
        <br/>
        <a href="#send">✏️ Написать сообщение</a><br/>
        <br/>
        <a href="chat.wml">↻ Обновить</a>
    </p>
</card>

<card id="send" title="Отправка сообщения">
    <p align="center">
        <strong>Новое сообщение</strong><br/>
        <br/>
        Введите текст:<br/>
        <input type="text" name="mes" size="20" maxlength="100" emptyok="false"/><br/>
        <br/>
        <anchor>📨 Отправить
            <go href="chat.wml" method="post">
                <postfield name="mes" value="$mes"/>
                <postfield name="action" value="send"/>
            </go>
        </anchor><br/>
        <br/>
        <a href="#chat">◀ Назад в чат</a>
    </p>
</card>

</wml>"""
    else:
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Чат</title>
    <meta http-equiv="refresh" content="5">
</head>
<body>
    <h1>Чат</h1>
    
    <div>
        {messages}
    </div>
    
    <hr>
    
    <form>
        <input type="text" name="mes" id="messageInput" placeholder="Сообщение">
        <button type="submit">Отправить</button>
    </form>

    <script>
        const input = document.getElementById('messageInput');
        
        // Загружаем сохранённый текст при загрузке страницы
        input.value = localStorage.getItem('draftMessage') || '';
        
        // Сохраняем текст при каждом изменении
        input.addEventListener('input', function() {{
            localStorage.setItem('draftMessage', this.value);
        }});
        
        // Очищаем сохранение после отправки (опционально)
        document.querySelector('form').addEventListener('submit', function() {{
            localStorage.removeItem('draftMessage');
        }});
    </script>
</body>
</html>'''

def tictactoe_menu():
    return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Крестики-нолики</title>
</head>
<body>
    <h1>Крестики-нолики</h1>
    
    <h3>Создать игру</h3>
    <form action="/ttt/game" method="GET">
        <button type="submit">Создать игру</button>
    </form>
    <br/>
    <br/>
    <br/>
    <form action="/ttt/game" method="GET">
        <label>Логин друга: <input type="text" name="log" placeholder="Логин друга"></label>
        <br><br>
        <button type="submit">Войти к другу</button>
    </form>
</body>
</html>'''

def tictactoe_wait(login: str):
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ожидание</title>
    <meta http-equiv="refresh" content="5">
</head>
<body>
    <h1>Вы создали лобби</h1>
    <h>Дайте другу ваш логин -{login}- для входа к вам</h>
    <form action="/game/exit">
        <button type="submit">Отменить игру</button>
    </form>
</body>
</html>'''

def tictactoe_game(login_enemy: str, map: str, is_step: bool):
    form_send_step = """<form action="/ttt/game">
        <label>Ваш ход: <input type="text" name="step" placeholder="Номер ячейки"></label>
        <button type="submit">Сделать ход</button>
    </form>""" if is_step else ''

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ожидание</title>
    <meta http-equiv="refresh" content="4">
</head>
<body>
    <h1>Крестики - Нолики</h1>
    <h>Ваш соперник: {login_enemy}</h> <br/>
    {map}
    {form_send_step}
    <br/>
    <form action="/ttt/game">
        <button type="submit">Сдаться</button>
    </form>
</body>
</html>'''

def error_join_game():
    return f'''<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Ожидание</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>Нет игрока с таким логином</h1>
        <h>Проверьте логин</h>
    </body>
    </html>'''

def winner_game(winner_string: str):
    return f'''<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Конец игры</title>
    </head>
    <body>
        <h1>{winner_string}</h1>
        <form action="/">
            <button type="submit">В главное меню</button>
        </form>
    </body>
    </html>'''
