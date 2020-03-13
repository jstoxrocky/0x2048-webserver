from flask import (
    Flask,
    jsonify,
)
from webserver.new_session import (
    new_session as endpoints_new_session,
)


application = Flask(__name__)


@application.route('/', methods=['GET'])
def index():
    message = {'name': 'Joey'}
    return jsonify(message)


@application.route('/new_session', methods=['GET'])
def new_session():
    payload = endpoints_new_session(None, None)
    return payload


if __name__ == '__main__':
    application.run(threaded=True)
