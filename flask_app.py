
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html', showthediv=0)


if __name__ == '__main__':
    app.run(debug=False)
