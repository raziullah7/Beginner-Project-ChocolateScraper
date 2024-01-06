import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        
        countries = response.xpath("//td/a")
        
        for country in countries:
            country_name = country.xpath(".//text()").get()
            # generates relative address
            link = country.xpath(".//@href").get()
        
            # converting to absolute address to pass
            abs_url = f'www.worldometers.info/{link}'   # approach 1
            abs_url = response.urljoin(link)            # approach 2
            # yield scrapy.Request(url=abs_url)         # approach 3
            
            # we can use the relative address as well
            # returns the <GET url> tag instead of just the full path
            # yield response.follow(url=link)           # approach 4
            
            # yield {
            #     'country_name': country_name,
            #     'link': response.urljoin(link)       # using approach 3
            # }
            
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': country_name})
    
    
    def parse_country(self, response):
        rows = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")
        
        # unnecessary because we found it in main parse()
        # country = response.xpath("//h2[1]/text()").get().replace("Population of ", "").replace(" (2024 and historical)", "")
        
        # getting the country name as argument from calling function
        country = response.request.meta['country_name']
        
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            
            yield {
                'country': country,
                'year': year,
                'population': population,
            }
