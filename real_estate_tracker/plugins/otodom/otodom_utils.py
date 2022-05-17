import re
import urllib
import json
import requests
from fake_useragent import UserAgent

from bs4 import BeautifulSoup, SoupStrainer

def get_user_agent(agent='chrome'):
    user_agent = UserAgent()
    return getattr(user_agent, agent)


def get_estate_ads(url):
    header = {'User-Agent': str(get_user_agent())}
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    base = "https://www.otodom.pl"
    pattern = r"^\/pl\/oferta\/.*"
    for a in soup.find_all('a', href=True):
        link = a['href']
        if(re.match(pattern, link)):
            link = urllib.parse.urljoin(base, link)
            links.append(link)
    
    return links


def get_ad_details(url):
    header = {'User-Agent': str(get_user_agent())}
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    details = {}
    
    estate_data = soup.find("script", {"id": "__NEXT_DATA__"})
    estate_data = str(estate_data.string)
    estate_data_json = json.loads(estate_data)
    
    details['url'] = url
    details['id'] = estate_data_json['props']['pageProps']['id']
    
    real_estate_characteristics = estate_data_json['props']['pageProps']['ad']['target']
    
    details['city'] = real_estate_characteristics['City']
    details['subregion'] = real_estate_characteristics['Subregion']
    details['province'] = real_estate_characteristics['Province']
    details['price'] = real_estate_characteristics['Price']
    details['price_per_sm'] = real_estate_characteristics['Price_per_m']
    details['area'] = real_estate_characteristics['Area']
    details['terrain_area'] = real_estate_characteristics.get('Terrain_area', 'UNKNOWN')
    details['build_year'] = real_estate_characteristics.get('Build_year', 'UNKNOWN')
    details['market_type'] = real_estate_characteristics['MarketType']
    details['number_of_rooms'] = real_estate_characteristics['Rooms_num'][0]
    
    return details
