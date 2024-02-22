# routes.py
from flask import Blueprint, render_template, request
from scraper import scrape_data
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

scrape_route = Blueprint('scrape_route', __name__)

def separate_city_code(city_name_or_code):
    if '(' in city_name_or_code:
        city_code = city_name_or_code.split(' (')[1][:-1]
        city_name = city_name_or_code.split(' (')[0]
    else:
        city_code = city_name_or_code[:3]
        city_name = city_name_or_code

    return city_code, city_name

def generate_agoda_url(date, departure_code, arrival_code):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    return_date_obj = date_obj + timedelta(days=1)
    return_date = return_date_obj.strftime("%Y-%m-%d")

    return f"https://www.agoda.com/en-in/flights/results?cid=1844104&departureFrom={departure_code}&departureFromType=1&arrivalTo={arrival_code}&arrivalToType=1&departDate={date}&returnDate={return_date}&searchType=1&cabinType=Economy&adults=1&sort=8"

def generate_easemytrip_url(date, departure_code, departure_name, arrival_code, arrival_name):
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    return f"https://flight.easemytrip.com/FlightList/Index?srch={departure_code}-{departure_name}-India|{arrival_code}-{arrival_name}-India|{formatted_date}&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=en-us&&IsDoubleSeat=false&CCODE=IN&curr=INR&apptype=B2C"

def generate_yatra_url(date, departure_code, arrival_code):
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    encoded_date = urllib.parse.quote(formatted_date, safe='')
    return f"https://flight.yatra.com/air-search-ui/dom2/trigger?ADT=1&CHD=0&INF=0&class=Economy&destination={arrival_code}&destinationCountry=IN&flexi=0&flight_depart_date={encoded_date}&hb=0&noOfSegments=1&origin={departure_code}&originCountry=IN&type=O&unique=663774921969&version=1.1&viewName=normal"

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

