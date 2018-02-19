from flask import (
    Flask,
    jsonify,
)
from flask_session import (
    Session,
)
from webserver.exceptions import (
    InvalidUsage,
)
from webserver.redis_session import (
    get_session,
)
from webserver.endpoints import (
    price,
    move,
    gamestate,
)


application = Flask(__name__)
SESSION_TYPE = 'redis'
SESSION_REDIS = get_session()
application.config.from_object(__name__)
Session(application)
API_PREFIX = '/api/v1'
application.register_blueprint(price.blueprint, url_prefix=API_PREFIX)
application.register_blueprint(move.blueprint, url_prefix=API_PREFIX)
application.register_blueprint(gamestate.blueprint, url_prefix=API_PREFIX)


@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    print(error.message)
    response = jsonify({'message': error.message})
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    application.run(threaded=True)
