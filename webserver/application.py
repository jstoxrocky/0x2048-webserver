from flask import (
    Flask,
    render_template,
)
from webserver.api import (
    api,
)


application = Flask(
    __name__,
    static_url_path='',
    static_folder='../static/dist',
    template_folder='../templates',
)
application.register_blueprint(api, url_prefix='/api/v1')


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
