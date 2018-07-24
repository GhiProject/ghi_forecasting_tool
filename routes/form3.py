from flask_app import app
from flask import render_template

@app.route('/form3')
def form3():
    return render_template('form3.html', showthediv='1')