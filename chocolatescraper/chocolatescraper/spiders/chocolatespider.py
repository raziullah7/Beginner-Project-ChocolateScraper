import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css('product-item')
        
        for product in products:
            result = product.css('span.price').get().split('£')
            yield {
                'name': product.css('a.product-item-meta__title::text').get(),
                'price': '£' + result[1].replace('</span>', '').strip(),
                'url': product.css('a.product-item-meta__title').attrib['href'],
            }

            # next_page = response.css('[rel="next"]').attrib['href']
            next_page = response.css('[rel="next"] ::attr(href)').get()
            
            if next_page is not None:
                # base website's url('https://www.chocolate.co.uk') + next page bit('/collections/all?page=2')
                yield response.follow('https://www.chocolate.co.uk' + next_page)
