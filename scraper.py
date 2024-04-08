import requests
from bs4 import BeautifulSoup
import time

class Scraper:
    def __init__(self, proxy=None):
        self.proxy = proxy

    def scrape(self, page_limit=None, retry_interval=10):
        base_url = "https://dentalstall.com/shop/"
        headers = {"User-Agent": "Mozilla/5.0"}
        products = []

        response = None

        for page_num in range(1, page_limit + 1) if page_limit else range(1, 5):
            url = base_url + f"/page/{page_num}/"
            for _ in range(3):  # Retry mechanism
                try:
                    response = requests.get(url, headers=headers, proxies={"http": self.proxy, "https": self.proxy} if self.proxy is not None else None)
                    if response.status_code == 200:
                        break
                except requests.exceptions.RequestException:
                    pass
                time.sleep(retry_interval)

            if response:
                soup = BeautifulSoup(response.content, "html.parser")
                product_cards = soup.find_all("div", class_="product-inner clearfix")

                for card in product_cards:
                    product_title = card.find("h2", class_="woo-loop-product__title").find("a").text.strip()
                    product_price = card.find("span", class_="price").text.strip().replace("₹", "").replace("Starting at:", "")
                    image_url = card.find("div", class_="mf-product-thumbnail").find("a").find("img")["data-lazy-src"]

                    products.append({
                        "product_title": product_title,
                        "product_price": product_price,
                        "path_to_image": image_url
                    })

        return products