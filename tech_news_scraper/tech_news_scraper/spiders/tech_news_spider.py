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

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]


    def parse(self, response):
        user_agent = response.request.headers["User-Agent"]
        print("**********************************")
        print(f"current user agent: {user_agent}")

        seen_urls = set()
        urls = response.css(
            "h2.wp-block-post-title a ::attr(href)").getall()
        
        for url in urls:
            if url not in seen_urls:
                seen_urls.add(url)
                yield response.follow(url, self.parse_article, headers={"User-Agent": random.choice(self.user_agents)})

        next_page = response.css(
            "a.post-picker-group-pagination__next ::attr(href)").get()
        
        if next_page:
            yield response.follow(next_page, self.parse , headers={"User-Agent": random.choice(self.user_agents)})

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

                        

            
           
        
