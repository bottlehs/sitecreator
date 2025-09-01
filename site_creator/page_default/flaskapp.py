from flask import Flask, render_template

import configparser
from handlers.pages import white, black



config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__, template_folder="./templates")
app.config['DEBUG'] = True

SITE = config['site']['SITE']
BLACK = config['site']['BLACK']
BLACK_LIST = config['site']['BLACK_LIST'].split(' ')


@app.route('/')
def home():
    if BLACK == "true":
        return black(BLACK_LIST)
    return white()


@app.route('/<random>/<routing>')
def web(random, routing):
    if BLACK == "true":
        return black(BLACK_LIST)
    return white()


if __name__ == '__main__':
    app.run()
