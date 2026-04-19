"""
guest - dict[ip str, (login - str, isButtonPhone - bool)]
"""
guests = dict()

def add_guest(ip: str, log: str, is_button_phone = False):
    if contains(ip):
        raise ValueError('ip contains in guests. But this function was call and from try add guest.')
    guests.setdefault(ip, (log, is_button_phone))

def contains(ip: str) -> bool:
    return ip in guests

def get_login(ip: str) -> str:
    if not contains(ip):
        raise Exception('Not user in session')
    return guests[ip][0]

def is_button_phone(ip: str) -> bool:
    if not contains(ip):
        raise Exception('Not user in session')
    return guests[ip][1]

def get_log_and_but(ip: str) -> tuple[str, bool]:
    if not contains(ip):
        raise Exception('Not user in session')
    return guests[ip]

def remove(ip: str):
    if not contains(ip):
        raise Exception('Not user in session')
    del guests[ip]