from flask import (
    Flask,
    jsonify,
)
import os


application = Flask(__name__)


@application.route('/', methods=['GET'])
def index():
    message = {'name': 'Joey'}
    return jsonify(message)


if __name__ == '__main__':
    # For Heroku
    application.run(threaded=True)
