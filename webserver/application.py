from flask import (
    Flask,
    request,
    render_template,
)
from webserver.new_session import (
    new_session as endpoints_new_session,
)
from webserver.new_game import (
    new_game as endpoints_new_game,
)
from webserver.move import (
    move as endpoints_move,
)


application = Flask(
    __name__,
    static_url_path='',
    static_folder='../static/dist',
    template_folder='../templates',
)


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@application.route('/new_session', methods=['GET'])
def new_session():
    payload = endpoints_new_session(None, None)
    return payload


@application.route('/new_game', methods=['POST'])
def new_game():
    event = request.get_json()
    payload = endpoints_new_game(event, None)
    return payload


@application.route('/move', methods=['POST'])
def move():
    event = request.get_json()
    payload = endpoints_move(event, None)
    return payload


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
