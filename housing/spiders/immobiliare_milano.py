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
        "https://www.immobiliare.it/ricerca.php?idCategoria=1&idContratto=1&idTipologia=4&idNazione=IT&prezzoMinimo=140000&prezzoMassimo=220000&superficieMinima=60&superficieMassima=140&localiMinimo=2&localiMassimo=3&tipoProprieta=1&noAste=1&pag=1&vrt=45.460316%2C9.238263%3B45.45868%2C9.239198%3B45.457367%2C9.240132%3B45.45491%2C9.242001%3B45.453598%2C9.242935%3B45.451305%2C9.244571%3B45.449177%2C9.246673%3B45.44852%2C9.247607%3B45.446552%2C9.251578%3B45.44508%2C9.255081%3B45.44475%2C9.25695%3B45.445732%2C9.260454%3B45.4477%2C9.262089%3B45.449665%2C9.26279%3B45.452454%2C9.263023%3B45.456223%2C9.263023%3B45.457367%2C9.263023%3B45.460316%2C9.262556%3B45.462284%2C9.261622%3B45.463593%2C9.261155%3B45.46589%2C9.260454%3B45.46769%2C9.260221%3B45.469654%2C9.259286%3B45.47244%2C9.258352%3B45.474243%2C9.257651%3B45.476208%2C9.257418%3B45.478172%2C9.25695%3B45.479156%2C9.256717%3B45.48194%2C9.256483%3B45.484398%2C9.256016%3B45.485542%2C9.256249%3B45.48882%2C9.256483%3B45.49144%2C9.256717%3B45.49275%2C9.25695%3B45.495697%2C9.257651%3B45.498478%2C9.258586%3B45.500114%2C9.259286%3B45.503227%2C9.2609215%3B45.504864%2C9.261622%3B45.507484%2C9.262556%3B45.510265%2C9.263958%3B45.51125%2C9.264192%3B45.514194%2C9.265594%3B45.51616%2C9.266294%3B45.51763%2C9.266994%3B45.520576%2C9.268163%3B45.52336%2C9.269096%3B45.524834%2C9.26933%3B45.529087%2C9.270031%3B45.532032%2C9.270265%3B45.533016%2C9.270498%3B45.53694%2C9.270498%3B45.539722%2C9.270498%3B45.540867%2C9.270498%3B45.54414%2C9.26933%3B45.54643%2C9.268163%3B45.5479%2C9.266994%3B45.549866%2C9.264659%3B45.55101%2C9.263724%3B45.55314%2C9.260454%3B45.555428%2C9.257418%3B45.556572%2C9.2555485%3B45.559025%2C9.251345%3B45.561153%2C9.246906%3B45.562134%2C9.245037%3B45.563606%2C9.242468%3B45.56475%2C9.240132%3B45.565403%2C9.238964%3B45.566547%2C9.236629%3B45.56769%2C9.233826%3B45.568184%2C9.232657%3B45.56933%2C9.229621%3B45.570965%2C9.226117%3B45.57211%2C9.223782%3B45.573578%2C9.220043%3B45.574722%2C9.21654%3B45.57538%2C9.2144375%3B45.57587%2C9.209766%3B45.57587%2C9.2083645%3B45.575214%2C9.204393%3B45.57407%2C9.200189%3B45.573578%2C9.198554%3B45.572598%2C9.195984%3B45.571453%2C9.193648%3B45.571125%2C9.192246%3B45.56998%2C9.189677%3B45.569%2C9.187108%3B45.568348%2C9.186173%3B45.567204%2C9.183604%3B45.565567%2C9.180801%3B45.565075%2C9.179633%3B45.56295%2C9.175662%3B45.561314%2C9.172626%3B45.560333%2C9.170991%3B45.558537%2C9.168654%3B45.55739%2C9.16702%3B45.55559%2C9.16445%3B45.55314%2C9.161413%3B45.55183%2C9.160479%3B45.548557%2C9.158143%3B45.545776%2C9.157208%3B45.544468%2C9.156976%3B45.54136%2C9.156976%3B45.53792%2C9.158143%3B45.536285%2C9.158844%3B45.53367%2C9.160479%3B45.532032%2C9.1618805%3B45.531216%2C9.162581%3B45.52958%2C9.163983%3B45.527943%2C9.165384%3B45.5268%2C9.166553%3B45.524178%2C9.169589%3B45.523197%2C9.170757%3B45.520412%2C9.173794%3B45.518124%2C9.176597%3B45.516975%2C9.177765%3B45.514687%2C9.179867%3B45.512394%2C9.182436%3B45.51092%2C9.185006%3B45.50945%2C9.188744%3B45.5083%2C9.19248%3B45.50781%2C9.194583%3B45.507156%2C9.198554%3B45.506336%2C9.202759%3B45.505848%2C9.204861%3B45.505028%2C9.209533%3B45.504208%2C9.213737%3B45.50372%2C9.215839%3B45.502407%2C9.2205105%3B45.500935%2C9.224482%3B45.500114%2C9.2258835%3B45.498478%2C9.227985%3B45.49766%2C9.22892%3B45.49422%2C9.2319565%3B45.492584%2C9.233358%3B45.49111%2C9.234058%3B45.48849%2C9.235694%3B45.485706%2C9.236862%3B45.484726%2C9.2373295%3B45.48243%2C9.238263%3B45.479973%2C9.238964%3B45.47883%2C9.239198%3B45.47637%2C9.239665%3B45.474407%2C9.239899%3B45.473095%2C9.240132%3B45.470146%2C9.240132%3B45.467197%2C9.240132%3B45.46589%2C9.240132%3B45.463593%2C9.239899%3B45.460316%2C9.238263&fasciaPiano%5B0%5D=20&fasciaPiano%5B1%5D=30&imm_source=bookmarkricerche&id=47221333"
    ]