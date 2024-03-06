# Flight Saver Pro 
![Premium Vector _ Plane ticket, airline boarding pass template_](https://github.com/adityakatre/FlightSaverPro/assets/85092727/150b07f9-3a6a-421b-a161-6fe1e839dcd7)

This project is a web scraping tool designed to gather flight data from three Online Travel Agencies (OTAs) for use in flight search applications. It collects data such as flight prices, departure times from the following OTAs:

1 Yatra.com 

2 Easemytrip.com

3 Agoda.com




## Installation

Before you begin, ensure you have Python installed on your system. This project is built with Flask, a Python web framework, and uses Selenium for web scraping, among other libraries.

### Step 1: Clone the Repository

Start by cloning this project to your local machine. Open a terminal and run:

```bash
git clone https://github.com/Adityakatre/FlightSaverPro.git
```
### Step 2:Install the required dependencies using pip:
```bash
pip install Flask 
pip install selenium
pip install bs4 
pip install urllib3
pip install datetime
pip install pandas
```
### Step 3:Install ChromeDriver 
 Ensure you have ChromeDriver installed for Selenium. You can download ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/ and add it to your system's PATH.
### Step 4: Run flask 
Run the Flask application. In your terminal, navigate to the project directory and run.Open a web browser and go to http://127.0.0.1:5000/ to view the application.


## Ethical Considerations

This project scrapes data from three Online Travel Agencies (OTAs), which, at the time of this writing, do not provide a `robots.txt` file specifying the rules for web scraping activities. While the absence of a `robots.txt` file might imply that the websites do not explicitly restrict web scraping, we have taken several steps to ensure that our scraping activities remain ethical and minimize potential harm or disruption to the website's operations:

- **Rate Limiting:** We ensure that our scraping requests are made at a reasonable interval, avoiding an excessive number of requests in a short period that could overwhelm the website's servers.
- **Data Minimization:** We only scrape data that is necessary for our project's objectives, avoiding the collection of personal or sensitive information.
- **User-Agent String:** Our scraper identifies itself with a clear user-agent string, allowing website administrators to identify the source of the scraping requests.
- **Compliance with Terms of Service:** We review and comply with the websites' Terms of Service, ensuring that our scraping activities do not violate their policies.

We encourage all users of this project to adhere to these principles and to conduct their own review of ethical considerations and legal compliance relevant to their use case.

## Legal Notice

This project is intended for educational and research purposes only. Users are responsible for ensuring that their use of the software complies with the websites' terms of service, local laws, and regulations. The maintainers of this project do not assume any responsibility for any misuse of the software or any violations of laws or terms of service.
