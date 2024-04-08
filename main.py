from fastapi import FastAPI

from scraper import Scraper
from scraper_manager import ScraperManager

from utils.database import Database as Storage
from utils.notifier import Notifier
from utils.authentication import Authentication


app = FastAPI()


@app.get("/scrape")
def read_root():

    # initialization of the classes
    scraper = Scraper()
    storage = Storage()
    notifier = Notifier()
    authentication = Authentication("your_static_token")
    scraper_manager = ScraperManager(scraper, storage, notifier, authentication)

    scraping_info = scraper_manager.scrape_and_store(page_limit=5, proxy="your_proxy_string", token="your_static_token")
    scraped_data = storage.get_existing_products()
    
    return {
        "info" : scraping_info,
        "data" : scraped_data
    }
