from flask import Flask
import sys

app = Flask(__name__)

sys.path.append("routes")
from main import *

if __name__ == '__main__':
    app.run(debug=False)
