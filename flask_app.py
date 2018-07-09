
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
import sys

app = Flask(__name__)

sys.path.append("routes")
from main import *

if __name__ == '__main__':
    app.run(debug=False)
