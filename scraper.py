import scrapy
import re
from scrapy.exceptions import CloseSpider


class GazzettaUfficialeSpider(scrapy.Spider):
    # let's give an italian name to this guy
    name = 'gilberto'

    start_urls = [
        # example URL:
        # "http://www.gazzettaufficiale.it/gazzetta/concorsi/caricaDettaglio/home?dataPubblicazioneGazzetta=2018-10-23&numeroGazzetta=84"
    ]   

    def __init__(self, *args, **kwargs):
        super(GazzettaUfficialeSpider, self).__init__(*args, **kwargs)
        """
            Overwrites default constructor to pass initial url
            This can be called as scrapy crawl gilberto -a start_url="http://some_url"
            Or otherwise This can be called as scrapy crawl gilberto -a start_urls="http://some_url1,http://some_url2"
        """
        if kwargs.get('start_urls') is not None:
            self.start_urls = kwargs.get('start_urls').split(',')
        elif kwargs.get('start_url') is not None:
            self.start_urls = [kwargs.get('start_url')]
        else:
            raise CloseSpider('Nothing to do! Please provide the URL using -a start_url="http://some_url" or -a start_urls="http://some_url1,http://some_url2"')

    def parse(self, response):
        for emettitore in response.css('span.emettitore'):

            # emettitore del bando o dei bandi
            emettitore_bando = emettitore.xpath("text()").extract()
            
            # take the inner value of the span tag
            for r in emettitore.xpath("following-sibling::span")[0].css("span.risultato"):
                body = re.sub(r"\s+", " ", "".join(r.xpath("a/text()").extract()))
                yield {
                    "emettitore" : emettitore_bando,
                    "body" : body,
                }