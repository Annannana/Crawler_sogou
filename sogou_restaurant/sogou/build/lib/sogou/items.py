import scrapy


class SogouItem(scrapy.Item):
    name = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    address = scrapy.Field()
    province = scrapy.Field()
    phone = scrapy.Field()
    city = scrapy.Field()
    fields = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    specialfood = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    province = scrapy.Field()
    category = scrapy.Field()
    tag = scrapy.Field()
    link = scrapy.Field()
