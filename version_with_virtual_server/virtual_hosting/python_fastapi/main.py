from flask import Flask, request

PASSWORD_SERVER = 'wig'

reload_page = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <!-- Reload every 1 second -->
    <meta http-equiv="refresh" content="1">
    <title>Auto Reload</title>
</head>
<body>
    <p>This page reloads every second.</p>
</body>
</html>
'''

count_check_server = 0
count_set_all_answer_server = 0

app = Flask(__name__)
application = app
reqs = dict()


class Request:
    """
    Represents a pending request from a client.

    Stores:
    - args: list of arguments sent by the client
    - answer: response that will be provided later by the server
    """

    def __init__(self, args: list):
        """
        Initialize a Request object.

        :param args: List of arguments received from the client
            if length arg < 2, then fill on none
        """
        while len(args) < 2:
            args.append('none')
        self.__args__ = args
        self.__answer__ = None

    @property
    def args(self):
        """
        Get the request arguments.

        :return: List of arguments
        """
        return self.__args__

    def set_answer(self, answer):
        """
        Set the response for this request.

        :param answer: Response string to send back to the client
        """
        self.__answer__ = answer

    @property
    def answer(self):
        """
        Get the stored answer.

        :return: Response string or None if not yet set
        """
        return self.__answer__

    def __str__(self):
        """
        String representation of the request.

        :return: Human-readable request info
        """
        return f"args: {self.__args__}, answer: {self.__answer__}"


@app.route('/get')
def for_client():
    """
    Endpoint for client polling.

    Behavior:
    - If client has a pending request:
        - Returns reload page if answer is not ready
        - Returns answer if ready and removes request
    - If no request exists:
        - Creates a new request and asks client to reload

    :return: HTML reload page or actual response
    """
    args = list(request.args.values())
    ip = request.remote_addr

    if ip in reqs:
        req = reqs[ip]
        if req.answer is None:
            return reload_page
        else:
            del reqs[ip]
            return req.answer
    else:
        req = Request(args)
        reqs.setdefault(ip, req)
        return reload_page


def login_root(args) -> bool:
    """
    Validate server authentication.

    :param args: Request arguments
    :return: True if password is correct, False otherwise
    """
    if not 'password' in args:
        return False
    elif request.args['password'] != PASSWORD_SERVER:
        return False
    return True


@app.route('/server/get')
def server_get_req():
    """
    Endpoint for server to fetch pending client requests.

    Requires authentication.

    Behavior:
    - Returns first pending request arguments
    - Returns 'none' if no requests exist

    :return: Semicolon-separated arguments or 'none'
    """
    if not login_root(request.args):
        return 'error'

    global count_check_server
    count_check_server += 1

    if len(reqs) > 0:
        ip = list(reqs.keys())[0]
        req = reqs[ip]
        return ip + ';' + ';'.join(req.args)
    else:
        return 'none'


@app.route('/server/send')
def server_send_answer():
    """
    Endpoint for server to send response using GET.

    Requires authentication.

    Behavior:
    - Sets answer for the first pending request
    - Returns status messages

    :return: 'ok', 'not requests', or error message
    """
    if not login_root(request.args):
        return 'error'

    global count_set_all_answer_server
    count_set_all_answer_server += 1

    if len(reqs) == 0:
        return 'not requests'
    if not 'answer' in request.args:
        return 'not answer'

    answer = request.args['answer']
    req = reqs[list(reqs.keys())[0]]
    req.set_answer(answer)
    return 'ok'


@app.route('/server/send', methods=['POST'])
def server_send_post_answer():
    """
    Endpoint for server to send response using POST.

    Requires authentication.

    Behavior:
    - Expects 'page' field in POST form data
    - Sets answer for the first pending request

    :return: 'ok', 'not requests', or error message
    """
    if not login_root(request.args):
        return 'error'

    global count_set_all_answer_server
    count_set_all_answer_server += 1

    if len(reqs) == 0:
        return 'not requests'
    if not 'page' in request.form:
        return 'not page answer in post request'

    answer = request.form.get('page')
    req = reqs[list(reqs.keys())[0]]
    req.set_answer(answer)
    return 'ok'


@app.route('/admin/info')
def admin_info():
    """
    Administrative endpoint to inspect server state.

    Requires authentication.

    Provides:
    - List of all pending requests with IPs
    - Counters for server operations

    :return: Debug information string
    """
    if not login_root(request.args):
        return 'error'

    requests_info = ''
    for ip, req in reqs.items():
        requests_info += f"ip:{ip} req:{req.__str__()},"

    return (
        f"requests:{requests_info};\n"
        f"count_check_server:{count_check_server};\n"
        f"count_answer_server:{count_set_all_answer_server}"
    )


if __name__ == '__main__':
    """
    Entry point of the application.

    Runs the Flask development server in debug mode.
    """
    app.run(debug=True, port=8080, host='0.0.0.0')