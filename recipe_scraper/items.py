# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    ingredients = scrapy.Field()
    prepTime = scrapy.Field()
    cookTime = scrapy.Field()
    totalTime = scrapy.Field()
    instructions = scrapy.Field()
