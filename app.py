# app.py
from flask import Flask, render_template
from routes import scrape_route

app = Flask(__name__)

app.register_blueprint(scrape_route)

if __name__ == '__main__':
    app.run(debug=True)
