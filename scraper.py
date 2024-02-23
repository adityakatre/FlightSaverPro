# scraper.py
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import urllib.parse
from datetime import datetime, timedelta

chrome_options = Options()
chrome_options.add_argument("--headless") 

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
    
    
def extract_flight_data_yatra(card_soup):
    # Scraping code for Yatra
    price_elem = card_soup.find('div', {'class': 'i-b tipsy fare-summary-tooltip fs-18'})
    flight_price = price_elem.text.strip() if price_elem else "Price not found"

    duration_elem = card_soup.find('p', {'class': 'fs-12 bold du mb-2'})
    flight_duration = duration_elem.text.strip() if duration_elem else "Duration not found"

    departure_time_elem = card_soup.find('div', {'class': 'i-b pr'})
    departure_time = departure_time_elem.text.strip() if departure_time_elem else "Departure time not found"

    departure_location_elem = card_soup.find_all('p', {'class': 'fs-10 font-lightgrey no-wrap city ellipsis'})
    departure_location = departure_location_elem[0].text.strip() if departure_location_elem else "Departure location not found"

    arrival_time_elem = card_soup.find('div', {'class': 'bold fs-15 mb-2 pr time'})
    arrival_time = arrival_time_elem.text.strip() if arrival_time_elem else "Arrival time not found"

    arrival_location_elem = card_soup.find_all('p', {'class': 'fs-10 font-lightgrey no-wrap city ellipsis'})
    arrival_location = arrival_location_elem[1].text.strip() if arrival_location_elem else "Arrival location not found"

    return {
        "Flight Price": flight_price,
        "Flight Duration": flight_duration,
        "Departure Time": departure_time,
        "Departure Location": departure_location,
        "Arrival Time": arrival_time,
        "Arrival Location": arrival_location,
        "Site": "Yatra"
    }



def extract_price_value(flight_data):
    price = flight_data['Flight Price']
    price_value = float(price.replace('INR', '').replace(',', ''))
    return price_value



def scrape_emt(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    flight_rows = driver.find_elements(By.XPATH, "//div[contains(@class,'col-md-12 col-sm-12 main-bo-lis pad-top-bot ng-scope')]")
    data_list = []

    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute("outerHTML")
        elementsoup = BeautifulSoup(elementHTML, 'html.parser')
        flight_data = extract_flight_data_EaseMyTrip(elementsoup)
        data_list.append(flight_data)

    driver.quit()
    return data_list

def scrape_agoda(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    flight_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'Box-sc-kv6pi1-0 bhCeID')]")
    data_list = []

    for card in flight_cards:
        card_html = card.get_attribute("outerHTML")
        card_soup = BeautifulSoup(card_html, 'html.parser')
        flight_data = extract_flight_data_agoda(card_soup)
        data_list.append(flight_data)

    driver.quit()
    return data_list

def scrape_yatra(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    flight_cards = driver.find_elements(By.XPATH, "//div[contains(@class ,'flightItem border-shadow pr')]")
    data_list = []

    for card in flight_cards:
        card_html = card.get_attribute("outerHTML")
        card_soup = BeautifulSoup(card_html, 'html.parser')
        flight_data = extract_flight_data_yatra(card_soup)
        data_list.append(flight_data)

    driver.quit()
    return data_list

def scrape_data(agoda_url, emt_url, yatra_url):
    # Running scraping functions in parallel
    with ThreadPoolExecutor() as executor:
        emt_future = executor.submit(scrape_emt, emt_url)
        agoda_future = executor.submit(scrape_agoda, agoda_url)
        yatra_future = executor.submit(scrape_yatra, yatra_url)

    # Combine data from all sites
    data_list_emt = emt_future.result()
    data_list_agoda = agoda_future.result()
    data_list_yatra = yatra_future.result()
    combined_data = data_list_emt + data_list_agoda + data_list_yatra

    # Sort combined data by flight price
    combined_data_sorted = sorted(combined_data, key=extract_price_value)

    return combined_data_sorted