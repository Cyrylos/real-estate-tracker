from datetime import datetime, timedelta, date
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd

from otodom.otodom_utils import get_estate_ads, get_ad_details

def otodom_to_csv_scrapper(urls):
    real_estate_data = []
    header = ['url', 'id', 'city', 'subregion', 'province', 'price', 'price_per_sm', 'area', 'terrain_area', 'build_year', 'market_type', 'number_of_rooms']
    for url in urls:
        ads = get_estate_ads(url)
        for ad in ads:
            ad_data = get_ad_details(ad)
            real_estate_data.append(ad_data)
    
    today = date.today()
    date_string = today.strftime("%Y_%m_%d")
    output_file = f"output/otodom/{date_string}.csv"
    
    real_estate_df = pd.DataFrame(real_estate_data)
    real_estate_df.to_csv(output_file)
    
        

with DAG('real_estate_dag', start_date=datetime(2022, 1, 1), schedule_interval="0 2 * * *", catchup=False) as dag:
    with open('config/real_estate_config.json') as config_file:
        config = json.load(config_file)
    otodom_urls = config['otodom_urls']
    otodom_scrapper = PythonOperator(task_id='otodom_scrapper', python_callable=otodom_to_csv_scrapper, op_args=[otodom_urls])
    otodom_scrapper
