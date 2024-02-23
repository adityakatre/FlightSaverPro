# routes.py
from flask import Blueprint, render_template, request
from scraper import scrape_data , separate_city_code ,generate_agoda_url,generate_easemytrip_url,generate_yatra_url
import pandas as pd


scrape_route = Blueprint('scrape_route', __name__)

@scrape_route.route('/')
def home():
    return render_template('index.html')

@scrape_route.route('/scrape')
def scrape():
    departure = request.args.get('departure')
    arrival = request.args.get('arrival')
    date = request.args.get('date')
    
    departure_code, departure_name = separate_city_code(departure)
    arrival_code, arrival_name = separate_city_code(arrival)
    
    agoda_url = generate_agoda_url(date, departure_code, arrival_code)
    easemytrip_url = generate_easemytrip_url(date, departure_code, departure_name, arrival_code, arrival_name)
    yatra_url = generate_yatra_url(date, departure_code, arrival_code)
    
    data_list = scrape_data(agoda_url, easemytrip_url, yatra_url)

    df = pd.DataFrame(data_list)
    df.to_csv('combined_flight_data.csv', index=False, encoding='utf-8')
    
    flight_data = pd.read_csv('combined_flight_data.csv')

    return render_template('index.html', flight_data=flight_data.to_dict('records'), agoda_url=agoda_url, easemytrip_url=easemytrip_url, yatra_url=yatra_url)

