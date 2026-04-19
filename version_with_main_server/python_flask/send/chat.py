messages = list()

def add_message(login: str, message: str):
    messages.append((login, message))

def get_all_messages():
    result = str()
    for login, message in messages:
        result += f"<b>{login}:</b> {message}<br>"
    return result