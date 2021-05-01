import grequests
from bs4 import BeautifulSoup
import pandas as pd

holiday_homes = []


def get_urls():
    urls = []
    for x in range(1, 29):
        urls.append(f'https://www.holidayfrancedirect.co.uk/search?board=sc&people=2&page={x}')
    return urls


def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp


def parse_data(resp):
    for r in resp:
        soup = BeautifulSoup(r.content, 'lxml')
        content = soup.find_all('div', {'class': 'property-grid-item'})
        for property in content:
            name = property.find('h2').text
            spec = property.find('p', {'class': 'property-spec'}).text
            price = property.find('div', {'class', 'property-pricing'}).text
            link = property.find('h2').find('a')['href']

            property_info = {
                'name': name,
                'spec': spec,
                'price': price,
                'link': link
            }
            holiday_homes.append(property_info)
    return holiday_homes


urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse_data(resp))
print(df.head())
df.to_csv('holiday-homes.csv', index=False)
