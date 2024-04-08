import json
import redis

class Database:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.data = []

    def store(self, products):
        if not isinstance(products, list):
            raise TypeError("Products must be provided as a list")
        
        for product in products:
            self._validate_product(product)

        self.cache_results(products)
        
        self.data.extend(products)
        self._write_to_json()

    def _write_to_json(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_existing_products(self):
        with open(self.filename, "r") as file:
            data = json.load(file)
        return data
    
    def _validate_product(self, product):
        if not isinstance(product, dict):
            raise TypeError("Each product must be provided as a dictionary")

        required_keys = {"product_title", "product_price", "path_to_image"}
        if not required_keys.issubset(product.keys()):
            raise ValueError("Each product must contain keys: 'product_title', 'product_price', 'path_to_image'")
        
        if not isinstance(product["product_title"], str):
            raise TypeError("Product title must be a string")

        if not isinstance(product["product_price"], str):
            raise TypeError("Product price must be a number")

        if not isinstance(product["path_to_image"], str):
            raise TypeError("Path to image must be a string")

    
    def cache_results(self, products):
        for product in products:
            if self._product_price_changed(product):
                self._update_redis_cache(product)

    def _product_price_changed(self, product):
        key = f"product:{product['product_title']}"
        cached_price = self.redis_client.get(key)
        if cached_price:
            return cached_price != product['product_price']
        return True

    def _update_redis_cache(self, product):
        key = f"product:{product['product_title']}"
        self.redis_client.set(key, product['product_price'])