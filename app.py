from flask import (
    Flask,
    render_template,
)
from api import (
    api,
)


app = Flask(
    __name__,
    static_url_path='',
    static_folder='static/dist',
    template_folder='templates',
)
app.register_blueprint(api, url_prefix='/api/v1')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
