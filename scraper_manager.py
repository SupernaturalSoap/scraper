class ScraperManager:
    def __init__(self, scraper, storage, notifier, authentication):
        self.scraper = scraper
        self.storage = storage
        self.notifier = notifier
        self.authentication = authentication

    def scrape_and_store(self, page_limit=None, proxy=None, retry_interval=10, token=None):
        if not self.authentication.authenticate(token):
            raise ValueError("Invalid authentication token")

        # self.scraper.proxy = proxy
        products = self.scraper.scrape(page_limit, retry_interval)
        for product in products:
            print(product)
        self.storage.cache_results(products)
        self.storage.store(products)
        self.notifier.notify(len(products), len(products))

        return {
            "scraped" : len(products),
            "inserted" : len(products)
        }