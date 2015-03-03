import scrapy, re
from tutorial.items import RecipeItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class AllRecipesSpider(CrawlSpider):
    name = "allRecipes"
    allowed_domains = ["allrecipes.com"]
    start_urls = [
        "http://allrecipes.com/Recipes/Main.aspx",
        # "http://allrecipes.com/Recipe/Worlds-Best-Lasagna",
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def filter_links(self, links):
        baseDomain = self.get_base_domain( self.response_url)
        filteredLinks = []
        for link in links:
            if link.url.find(baseDomain) < 0:
                filteredLinks.append(link)
        return filteredLinks

    def my_process_value(value):
        m = re.search('recipes/main\.aspx\?Page=\d+', value, re.I)
        if m:
            print value
            return True
        else:
            return None

    rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'.*recipes/main\.aspx\?Page=\d+.*'), unique=True, process_value=my_process_value), callback='parse_page'),
        Rule(LinkExtractor(allow=(r'.*Detail\.aspx.*', ), unique=True), callback='parse_item')
    )

    def parse_item(self, response):
        # self.log('Hi, this is an item page! %s' % response.url)

        item = RecipeItem()

        item['title'] = response.xpath("//h1[@id = 'itemTitle']/text()").extract()[0]

        ingr = {}
        for sel in response.xpath("//p[contains(@itemprop,'ingredients')]"):
            amount = sel.xpath("span[@id='lblIngAmount']/text()").extract()
            name = sel.xpath("span[@id='lblIngName']/text()").extract()[0]

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
        self.log('Hi, this is a page!!!!!!!!!!!!!!!!!!!!!!! %s' % response.url)
