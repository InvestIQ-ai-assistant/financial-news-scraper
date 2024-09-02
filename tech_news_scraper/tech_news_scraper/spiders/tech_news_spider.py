import scrapy
import random

class TechNewsSpiderSpider(scrapy.Spider):
    name = "tech_news_spider"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com"]

    custom_settings = {
        "FEEDS":{
            "tech_news.json": {
                "format": "json",
                "overwrite": True
            }
        }
    }

    

    def parse(self, response):
        print("**********************************")
        user_agent = response.request.headers["User-Agent"]
        print(f"current user agent: {user_agent}")
       
        seen_urls = set()
        urls = response.css(
            "h2.wp-block-post-title a ::attr(href)").getall()
        
        for url in urls:
            if url not in seen_urls:
                seen_urls.add(url)
                yield response.follow(url, self.parse_article)

        next_page = response.css(
            "a.post-picker-group-pagination__next ::attr(href)").get()
        
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        print("**********************************")
        user_agent = response.request.headers["User-Agent"]
        print(f"current user agent: {user_agent}")
        category = response.css("a.is-taxonomy-category ::text").get()
        title = response.css("h1.wp-block-post-title ::text").get()
        date_time = response.css("div.wp-block-post-date time ::text").get()
        url = response.url
        paragraphs = response.css("div.wp-block-post-content p ::text").getall()
        combined_paragraphs_text = " ".join(paragraphs).strip()

        yield {
            "category": category,
            "title": title,
            "date_time": date_time,
            "url": url,
            "content": combined_paragraphs_text
        }

                        

            
           
        
