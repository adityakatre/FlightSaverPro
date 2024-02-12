# routes.py
from flask import Blueprint, render_template
from scraper import scrape_data
import pandas as pd

scrape_route = Blueprint('scrape_route', __name__)

@scrape_route.route('/')
def home():
    return render_template('index.html')

@scrape_route.route('/scrape')
def scrape():
    data_list = scrape_data()

    # Save to CSV
    df = pd.DataFrame(data_list)
    df.to_csv('combined_flight_data.csv', index=False, encoding='utf-8')

    # Read the CSV for display
    flight_data = pd.read_csv('combined_flight_data.csv')

    return render_template('index.html', flight_data=flight_data.to_dict('records'))
