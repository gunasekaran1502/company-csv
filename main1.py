import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


base_url = "https://www.yellowpages.com/search?search_terms=software+company&geo_location_terms=East+China%2C+MI"


data = []


def scrape_company_details(company):
    try:
        name = company.find('h2').text.strip() if company.find('h2') else 'N/A'
        phone = company.find('div', class_='is24x7').text.strip() if company.find('div', class_='is24x7') else 'N/A'
        address = company.find('span', class_='street-address').text.strip() if company.find('span', class_='street-address') else 'N/A'
        website = company.find('a', class_='track-visit-website')['href'] if company.find('a', class_='track-visit-website') else 'N/A'

        return {
            'Company Name': name,
            'Phone Number': phone,
            'Address': address,
            'Website': website
        }
    except Exception as e:
        print(f"Error scraping company details: {e}")
        return None


response = requests.get(base_url)
if response.status_code == 200:
    print("Successfully retrieved the page.")
else:
    print(f"Failed to retrieve the page: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
companies = soup.find_all('div', class_='result')

print(f"Found {len(companies)} companies.")


for company in companies:
    company_data = scrape_company_details(company)
    if company_data:
        data.append(company_data)

    time.sleep(1)


df = pd.DataFrame(data)


if not df.empty:
    df.to_csv('mobile_al_software_companies.csv', index=False)
    print("Data saved to 'mobile_al_software_companies.csv'.")
else:
    print("No data was collected.")


print(df)
