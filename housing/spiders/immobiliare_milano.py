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
        next_page = response.css(
            "#listing-pagination .pull-right li a::attr(href)"
        ).get()
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
        "https://www.immobiliare.it/ricerca.php?idCategoria=1&idContratto=1&idNazione=IT&prezzoMinimo=140000&prezzoMassimo=220000&superficieMinima=60&superficieMassima=140&localiMinimo=2&localiMassimo=3&criterio=rilevanza&ordine=desc&tipoProprieta=1&noAste=1&ascensore=1&pag=1&vrt=45.442345,9.25957;45.442345,9.257113;45.442345,9.255148;45.442863,9.251217;45.443897,9.247286;45.44424,9.245565;45.445274,9.2421255;45.446655,9.238932;45.447517,9.237212;45.44924,9.235001;45.451138,9.233035;45.453377,9.231316;45.45441,9.230578;45.456654,9.229104;45.459236,9.228367;45.461132,9.228122;45.463547,9.227631;45.465614,9.227385;45.46665,9.2271385;45.46923,9.2271385;45.47216,9.2271385;45.47457,9.2271385;45.476124,9.2271385;45.478706,9.2271385;45.481636,9.2271385;45.483185,9.226892;45.486286,9.226401;45.489044,9.22591;45.49042,9.225419;45.493347,9.224436;45.495243,9.223699;45.496964,9.222716;45.497826,9.221979;45.500237,9.219522;45.502476,9.216083;45.503338,9.214117;45.50523,9.210431;45.50592,9.207728;45.506783,9.204043;45.507126,9.202569;45.507812,9.198884;45.508846,9.194216;45.509365,9.191513;45.510914,9.187091;45.512634,9.183651;45.513668,9.182177;45.515217,9.17972;45.517113,9.177754;45.519005,9.175297;45.52021,9.174068;45.52245,9.171366;45.52503,9.168663;45.526234,9.167927;45.529335,9.166206;45.532085,9.165469;45.53312,9.165224;45.536045,9.164732;45.539658,9.164732;45.54241,9.164732;45.543446,9.164732;45.546886,9.165224;45.550327,9.166206;45.551876,9.166944;45.554283,9.168418;45.556522,9.170383;45.558243,9.172103;45.560307,9.175297;45.562885,9.179229;45.564606,9.182668;45.565296,9.183651;45.566326,9.186108;45.567875,9.189548;45.56822,9.190776;45.569595,9.195199;45.570454,9.198638;45.570797,9.20085;45.571144,9.205272;45.571316,9.209203;45.571487,9.21338;45.57166,9.214854;45.57166,9.21903;45.57166,9.221979;45.57166,9.223945;45.571487,9.228122;45.571316,9.23107;45.570972,9.235001;45.570625,9.236966;45.569595,9.241143;45.56856,9.244092;45.568047,9.24532;45.56667,9.248268;45.56512,9.251217;45.56392,9.253182;45.56237,9.255393;45.560993,9.2573595;45.55893,9.25957;45.55807,9.260307;45.55566,9.262519;45.55239,9.2647295;45.551533,9.265222;45.549297,9.26645;45.545853,9.268169;45.544132,9.268907;45.54138,9.270135;45.537766,9.270872;45.5357,9.271118;45.53381,9.271118;45.530884,9.271118;45.528816,9.271118;45.526924,9.271118;45.52365,9.270872;45.520725,9.270381;45.519695,9.270381;45.517456,9.26989;45.514874,9.269644;45.512634,9.268907;45.511257,9.268907;45.509018,9.268169;45.506783,9.267923;45.50575,9.267432;45.50351,9.266941;45.50127,9.266941;45.49903,9.26645;45.498173,9.265958;45.496277,9.265713;45.493866,9.265958;45.49266,9.265713;45.49042,9.265467;45.48784,9.265222;45.486805,9.264976;45.484737,9.264484;45.48215,9.2647295;45.47957,9.264484;45.47819,9.264484;45.47578,9.264238;45.473194,9.264238;45.47216,9.264238;45.46992,9.264238;45.46699,9.264238;45.465267,9.263992;45.462685,9.263992;45.459755,9.263992;45.456825,9.263992;45.45579,9.263747;45.453033,9.26301;45.450275,9.262273;45.44838,9.261782;45.44545,9.260062;45.44269,9.257113&fasciaPiano[]=20&fasciaPiano[]=30"
    ]