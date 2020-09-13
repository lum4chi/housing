import re
import json
import scrapy
from housing.utils import dict_filter


class ImmobiliareMilanoSpider(scrapy.Spider):
    name = "immobiliare-milano"
    allowed_domains = ["immobiliare.it"]
    # This will crawl a huge number of houses, use with discretion!
    start_urls = [
        "https://www.immobiliare.it/ricerca.php?idCategoria=1&idContratto=1&idNazione=IT&raggio=11983.347766088&criterio=rilevanza&ordine=desc&tipoProprieta=1&noAste=1&pag=1&centro=45.469762,9.181137"
    ]
    english_translation = {
        "locali": "rooms",
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
            url = house.css("a").xpath("@href").get()
            features_keys = list(map(str.strip, house.css(".lif__text::text").getall()))
            features_keys = [
                str(self.english_translation.get(f)) for f in features_keys
            ]
            features_vals = list(
                map(str.strip, house.css(".lif__data .text-bold::text").getall())
            )
            yield scrapy.Request(
                url,
                callback=self.parse_house_details,
                cb_kwargs={k: v for k, v in zip(features_keys, features_vals)},
            )
        next_page = response.css(
            "#listing-pagination .pull-right li a::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_house_details(self, response, **kwargs):
        listing_item = json.loads(response.css("#js-hydration::text").get())["listing"]
        dict_filter(listing_item)
        listing_item.update(**kwargs)
        yield listing_item


class FilteredImmobiliareMilanoSpider(ImmobiliareMilanoSpider):
    name = "immobiliare-milano-filtered"
    # Hint: do your search from the website and then copy/paste url
    start_urls = [
        "https://www.immobiliare.it/ricerca.php?idCategoria=1&idContratto=1&idNazione=IT&prezzoMinimo=120000&prezzoMassimo=280000&raggio=11983.347766088&localiMinimo=2&localiMassimo=3&criterio=rilevanza&ordine=desc&tipoProprieta=1&noAste=1&pag=1&centro=45.469762,9.181137"
    ]