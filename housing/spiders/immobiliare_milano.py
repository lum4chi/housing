import scrapy
import re
from housing.items import HousingItem


class ImmobiliareMilanoSpider(scrapy.Spider):
    __version__ = "20200911"
    name = "immobiliare-milano"
    allowed_domains = ["immobiliare.it"]
    # Do your search and then copy/paste url
    start_urls = ["https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza"]
    english_translation = {
        "locali": "room",
        "superficie": "area",
        "bagni": "baths",
        "piano": "floor",
        "unità": "unit",
        "immobile": "real estate",
        "garantito": "guaranteed",
    }

    def parse(self, response):
        houses = response.css(".listing-item_body")
        for house in houses:
            title = house.css("a::text").get().strip()
            url = house.css("a").xpath("@href").get()
            _id = re.match("https://www.immobiliare.it/annunci/(.*)/", url).groups()[0]
            price = house.css(".lif__pricing::text").get()
            if price is None:
                # Sometimes they want to show a older/newer price
                price = house.css(".lif__pricing div::text").get()
            price = price.strip() if price is not None else None
            features_keys = list(map(str.strip, house.css(".lif__text::text").getall()))
            features_keys = [
                str(self.english_translation.get(f)) for f in features_keys
            ]
            features_vals = list(
                map(str.strip, house.css(".lif__data .text-bold::text").getall())
            )
            yield dict(
                _id=_id,
                title=title,
                price=price,
                **{k: v for k, v in zip(features_keys, features_vals)}
            )
        next_page = response.css(
            "#listing-pagination .pull-right li a::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
