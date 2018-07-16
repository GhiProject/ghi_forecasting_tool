from flask_app import app
from flask import render_template

@app.route('/form')
def form():
    return render_template('form.html')