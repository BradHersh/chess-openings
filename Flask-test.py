import chess
import random
import time
from IPython.display import display, HTML, clear_output

from flask import Flask, render_template, request, jsonify
app = Flask(__name__, template_folder = 'templates')

def display_board(board):
    return "<pre>" + str(board) + "</pre>"


def execute():
    board = chess.Board()
    return display_board(board)


@app.route('/')
def home ():
    return render_template('index.html', x= execute())



if __name__ == "__main__":
    app.run()


