from flask import Flask, render_template
import configparser
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handlers.pages import white, black



config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__, template_folder="./templates")
app.config['DEBUG'] = True

# 설정 파일 읽기 오류 처리
try:
    SITE = config['site']['SITE']
    BLACK = config['site']['BLACK']
    BLACK_LIST = config['site']['BLACK_LIST'].split(' ')
except KeyError as e:
    print(f"설정 파일 오류: {e}")
    SITE = ""
    BLACK = ""
    BLACK_LIST = []


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
