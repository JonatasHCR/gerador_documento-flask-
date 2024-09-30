from flask import Flask

from routes.home import home_route
from routes.word import word_route

app = Flask(__name__)

app.register_blueprint(home_route)
app.register_blueprint(word_route, url_prefix='/word')

app.run(debug=True)