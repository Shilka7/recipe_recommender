import scrapy, re
from recipe_scraper.items import RecipeItem
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class AllRecipesSpider(CrawlSpider):
    name = "allRecipes"
    allowed_domains = ["allrecipes.com"]
    start_urls = [
        "http://allrecipes.com/recipes/main.aspx?Page=%d#recipes" % i for i in xrange(1,51)
        # "http://allrecipes.com/Recipe/Worlds-Best-Lasagna",
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]


    def my_process_value(value):
        m = re.search('recipes/main\.aspx\?Page=\d+', value, re.I)

        if m:
            print
            return value
        else:
            return None

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(process_value=my_process_value, restrict_xpaths=("//div[contains(@class,'page_navigation_nav')]")), callback='parse_page'),
        Rule(LinkExtractor(allow=(r'.*Detail\.aspx.*1$', ), unique=True), callback='parse_item'),
    )

    def parse_item(self, response):
        # self.log.msg('Hi, this is an item page! %s' % response.url, log.DEBUG)

        item = RecipeItem()

        item['title'] = response.xpath("//h1[@id = 'itemTitle']/text()").extract()[0]

        ingr = {}
        for sel in response.xpath("//p[contains(@itemprop,'ingredients')]"):
            amount = sel.xpath("span[@id='lblIngAmount']/text()").extract()
            name = sel.xpath("span[@id='lblIngName']/text()").extract()[0]

            if not re.search("nbsp", name) and amount:
                ingr[name] = amount
            # item['link'] = sel.xpath('a/@href').extract()
            # item['desc'] = sel.xpath('text()').extract()
        item['ingredients'] = ingr

        item ['prepTime'] = []
        item ['cookTime'] = []
        item ['totalTime'] = []

        for span in response.xpath("//li[contains(@id,'liPrep')]/span"):
            item['prepTime'].append(span.xpath("em/text()").extract()[0] + span.xpath("text()").extract()[0])

        for span in response.xpath("//li[contains(@id,'liCook')]/span"):
            item['cookTime'].append(span.xpath("em/text()").extract()[0] + span.xpath("text()").extract()[0])

        for span in response.xpath("//li[contains(@id,'liTotal')]/span"):
            item['totalTime'].append(span.xpath("em/text()").extract()[0] + span.xpath("text()").extract()[0])

        instrList = []
        for dirSelector in response.xpath("//div[contains(@itemprop,'recipeInstructions')]//li"):
            instrList.append(dirSelector.xpath("span/text()").extract()[0])

        item['instructions'] = instrList
        yield item

    def parse_page(self, response):
        log.start("log.txt", log.DEBUG, True)
        log.msg('Hi, this is a page!!!!!!!!!!!!!!!!!!!!!!! %s' % response.url, level=log.DEBUG)
