import scrapy


class MovieItem(scrapy.Item):
    douban_id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    summary = scrapy.Field()
    poster_url = scrapy.Field()
    genres = scrapy.Field()       # list[str]
    countries = scrapy.Field()    # list[str]
    languages = scrapy.Field()    # list[str]
    directors = scrapy.Field()    # list[dict]  each: {douban_id, name}
    writers = scrapy.Field()      # list[dict]
    actors = scrapy.Field()       # list[dict]  each: {douban_id, name, role_name}
    related_movie_ids = scrapy.Field()  # list[str]


class PersonItem(scrapy.Item):
    douban_id = scrapy.Field()
    name = scrapy.Field()
    alias = scrapy.Field()
    gender = scrapy.Field()
    birth_year = scrapy.Field()
    birthplace = scrapy.Field()
