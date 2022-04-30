import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt1606375/']
    def parse (self,response):
        """
        navigates from the movie page to the cast and crew page
        """
        castCrewPageVar = 'fullcredits'
        nextCastCrewPage = response.urljoin(castCrewPageVar)
        if nextCastCrewPage:
            yield scrapy.Request(nextCastCrewPage, callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        links = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for link in links:
            specificCastPage = response.urljoin(link)
            yield scrapy.Request(specificCastPage,callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        #actor and tv show name
        actorName = response.css("span.itemprop::text ").get()
        movieTitles = response.css("div.filmo-row b a::text ").getall()

        for movie in movieTitles:
            yield {
                "Actor":actorName,
                "Movie/TV Show": movie
            }
        
