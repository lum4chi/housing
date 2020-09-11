import scrapy
import re
from itertools import zip_longest
from housing.items import HousingItem


class ImmobiliareMilanoSpider(scrapy.Spider):
    __version__ = "20200911"
    name = "immobiliare-milano"
    allowed_domains = ["immobiliare.it"]
    # Do your search and then copy/paste url
    start_urls = ["https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza"]

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
            rooms_area_baths = dict(
                zip_longest(
                    ["rooms", "area", "baths"],
                    map(str.strip, house.css(".lif__data span::text").getall()),
                )
            )
            floor = house.css(".lif__data abbr::text").get()
            if floor is None:
                floor = "0"
            floor = floor.strip()
            yield dict(
                _id=_id,
                title=title,
                # url=url,
                price=price,
                floor=floor,
                **rooms_area_baths
            )
        next_page = response.css(
            "#listing-pagination .pull-right li a::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
