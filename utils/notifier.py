class Notifier:
    def notify(self, num_scraped, num_updated):
        print(f"Scraping status: {num_scraped} products scraped, {num_updated} products updated in the database.")
