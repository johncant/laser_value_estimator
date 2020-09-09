import scrapy


class ApolloDuckSpider(scrapy.Spider):

    name = 'apolloduckspider'
    start_urls = ['https://laser.apolloduck.co.uk/boats/laser/laser-1']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1},
        'IMAGES_STORE': 'images'
    }

    def parse(self, response):

        advert_links = response.xpath("//div[@class='viewDetails']/..")
        pagination_links = response.xpath("//div[@class='paginate']//a")

        yield from response.follow_all(advert_links, self.parse_advert)
        yield from response.follow_all(pagination_links, self.parse)

    def parse_advert(self, response):

        advert_id = response.url.split('/')[-1]

        description_elem = response.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' featureSection ')]/h3[text()='Description']/..")[0]
        description_html = description_elem.getall()

        price = response.xpath("//*[@class='boatAdvertPrice']/text()").getall()[0].strip()
        image_urls = response.xpath("//*[@class='featureImage']//img/@data-src").getall()
        title = response.xpath("//*[@class='boatAdvertTitle']/text()").getall()[0].strip()

        return {
            'title': title,
            'description_html': description_html,
            'price': price,
            'image_urls': image_urls
        }
