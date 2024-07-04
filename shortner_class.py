import string
import random
from configs.config import settings

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
        return short_url

    def _generate_short_url(self):
        return "".join(random.choice(self.chars) for _ in range(self.short_url_length))

    def get_original_url(self, short_url):
        return self.url_map.get(short_url)


if __name__ == "__main__":
    shortener = URLShortener()
    short_url = shortener.shorten_url("https://example.com")
    print("Short URL:", short_url)
