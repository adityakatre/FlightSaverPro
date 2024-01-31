from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import time

app = Flask(__name__)


def extract_flight_data_EaseMyTrip(elementsoup):
    # Extracting flight price
    price_span = elementsoup.find('span', {'id': re.compile(r'spnPrice\d+')})
    flight_price = price_span.text.strip() if price_span else "Price not found"

    # Extracting flight time duration
    duration_span = elementsoup.find('span', {'class': 'dura_md'})
    flight_duration = duration_span.text.strip() if duration_span else "Duration not found"

    # Extracting flight timing
    departure_time_span = elementsoup.find('span', {'class': 'txt-r2-n ng-binding'})
    departure_location_span = elementsoup.find('span', {'class': 'txt-r3-n ng-binding'})
    arrival_time_span = elementsoup.find_all('span', {'class': 'txt-r2-n ng-binding'})[-1]
    arrival_location_span = elementsoup.find_all('span', {'class': 'txt-r3-n ng-binding'})[-1]

    departure_time = departure_time_span.text.strip() if departure_time_span else "Departure time not found"
    departure_location = departure_location_span.text.strip() if departure_location_span else "Departure location not found"
    arrival_time = arrival_time_span.text.strip() if arrival_time_span else "Arrival time not found"
    arrival_location = arrival_location_span.text.strip() if arrival_location_span else "Arrival location not found"

    return {
        "Flight Price": flight_price,
        "Flight Duration": flight_duration,
        "Departure Time": departure_time,
        "Departure Location": departure_location,
        "Arrival Time": arrival_time,
        "Arrival Location": arrival_location,
        "Site":"EaseMyTrip"
    }
    
    
def extract_flight_data_agoda(card_soup):

    price_elem = card_soup.find('span', {'class': 'FlightPrice__price--d9oH7'})
    flight_price = price_elem.text.strip() if price_elem else "N/A"

    departure_time_elem = card_soup.find('span', {'data-component': 'mob-flight-cardSliceDepartureTime'})
    departure_time = departure_time_elem.text.strip() if departure_time_elem else "N/A"

    departure_location_elem = card_soup.find('span', {'data-component': 'mob-flight-cardSliceOrigin'})
    departure_location = departure_location_elem.text.strip() if departure_location_elem else "N/A"

    arrival_time_elem = card_soup.find('span', {'data-component': 'mob-flight-cardSliceArrivalTime'})
    arrival_time = arrival_time_elem.text.strip() if arrival_time_elem else "N/A"

    arrival_location_elem = card_soup.find('span', {'data-component': 'mob-flight-cardSliceDestination'})
    arrival_location = arrival_location_elem.text.strip() if arrival_location_elem else "N/A"

    duration_elem = card_soup.find('span', {'data-component': 'mob-flight-cardSegmentDuration'})
    flight_duration = duration_elem.text.strip() if duration_elem else "N/A"
    
    return{"Flight Price": flight_price,
        "Flight Duration": flight_duration,
        "Departure Time": departure_time,
        "Departure Location": departure_location,
        "Arrival Time": arrival_time,
        "Arrival Location": arrival_location,
        "Site":"agoda"
    }

def scrape_data():
    # EaseMyTrip
    driver_emt = webdriver.Chrome()
    url_emt = "https://flight.easemytrip.com/FlightList/Index?srch=PNQ-Pune-India|DEL-Delhi-India|01/03/2024&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=en-us&&IsDoubleSeat=false&CCODE=IN&curr=INR&apptype=B2C"
    driver_emt.get(url_emt)
    time.sleep(5)
    flight_rows_emt = driver_emt.find_elements(By.XPATH, "//div[contains(@class,'col-md-12 col-sm-12 main-bo-lis pad-top-bot ng-scope')]")
    data_list_emt = []

    for WebElement in flight_rows_emt:
        elementHTML = WebElement.get_attribute("outerHTML")
        elementsoup = BeautifulSoup(elementHTML, 'html.parser')
        flight_data = extract_flight_data_EaseMyTrip(elementsoup)
        data_list_emt.append(flight_data)

    driver_emt.quit()

    # Agoda
    driver_agoda = webdriver.Chrome()
    url_agoda = "https://www.agoda.com/flights/results?cid=1891461&departureFrom=PNQ&departureFromType=1&arrivalTo=DEL&arrivalToType=1&departDate=2024-03-01&returnDate=2024-03-02&searchType=1&cabinType=Economy&adults=1&sort=8&tag=3cda3586-9ec8-88d2-2819-7b1e8bb3ad04&gclid=Cj0KCQiAkeSsBhDUARIsAK3tiececkb7ZE7VDSCv1G3_jea0qgR2fY8bsiAznIThLKsj6TW-7AzYXzAaAg6rEALw_wcB&site_id=1891461"
    driver_agoda.get(url_agoda)
    time.sleep(5)
    flight_cards_agoda = driver_agoda.find_elements(By.XPATH, "//div[contains(@class, 'Box-sc-kv6pi1-0 bhCeID')]")
    data_list_agoda = []

    for card in flight_cards_agoda:
        card_html = card.get_attribute("outerHTML")
        card_soup = BeautifulSoup(card_html, 'html.parser')
        flight_data = extract_flight_data_agoda(card_soup)
        data_list_agoda.append(flight_data)

    driver_agoda.quit()

    # Combine data
    combined_data = data_list_emt + data_list_agoda
    return combined_data

def save_to_csv(data_list, filename):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False, encoding='utf-8')

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle scraping and display sorted results
@app.route('/scrape')
def scrape():
    data_list = scrape_data()

    # Save to CSV
    save_to_csv(data_list, 'combined_flight_data.csv')

    # Read the CSV for display
    flight_data = pd.read_csv('combined_flight_data.csv')

    return render_template('index.html', flight_data=flight_data.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)