import string
import random
from configs.config import settings
from mongodb import MongoDBProgress
from console_log import create_log_app


console_log = create_log_app()
mongo_cls = MongoDBProgress()


# TODO: Objede tutma dbde tut
# TODO: shorten ayır ayrı proje olsun
class URLShortener:
    chars = string.ascii_letters + string.digits
    url_map = {}
    short_url_length = settings.shortner.URL_LENGTH

    def shorten_url(self, original_url):
        short_url = self._generate_short_url()
        while short_url in self.url_map:
            short_url = self._generate_short_url()
        self.url_map[short_url] = original_url
        mongo_cls.insert_data_to_collection(database_name=settings.mongo.DATABASE, collection_name="short_urls", data={"short_url": short_url, "original_url": original_url})
        return short_url

    def _generate_short_url(self):
        return "".join(random.choice(self.chars) for _ in range(self.short_url_length))

    def get_original_url(self, short_url):
        res = mongo_cls.get_data(database_name=settings.mongo.DATABASE, collection_name="short_urls", query={"short_url": short_url})
        return res.get("original_url", None)


def mongo_db_initial():
    mongo_cls.create_collection(database_name=settings.mongo.DATABASE, collection_name="short_urls")


if __name__ == "__main__":
    mongo_db_initial()
    shortener = URLShortener()
    short_url = shortener.shorten_url("https://example.com")
    print("Short URL:", short_url)
