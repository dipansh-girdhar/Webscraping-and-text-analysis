import scrapy
from scrapy.crawler import CrawlerProcess

# Trip Advisor Spider class
class TASpider(scrapy.Spider):

    # variable name
    name = "taspider"

    # start_requests method: to define which websites to scrape
    def start_requests(self):

        # list of webpages to scrape
        # Note: Just added three more pages which are different reviews page numbers of the same restaurant
        #  so that we don't miss anything
        
        urls = [ "https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html",
        "https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews-or130-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html",
        "https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews-or80-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html",
        "https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews-or180-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html" ]
        # follow the links to the next parser
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_front)

    # parse_front method: to parse the front page
    def parse_front(self, response):

        # narrow down on the page block elements
        page_blocks = response.css('div.pageNumbers')
        # direct to the page links
        page_links = page_blocks.xpath('./a/@href')
        # extract the links
        links_to_follow = page_links.extract()
        print("\nNumber of pages\n")
        print(len(links_to_follow))
        # follow the links to the next parser
        for link in links_to_follow:
            yield response.follow(url=link, callback=self.parse_second)
    
    def parse_second(self, response):
        #narrow down to eaach review
        review_blocks=response.css('div.quote')
        review_links=review_blocks.xpath('./a/@href')
        review_links=review_links.extract()

        for link in review_links:
            yield response.follow(url=link, callback=self.parse_pages)

    # parse_pages method: to parse the pages
    def parse_pages(self, response):

        # direct to the review title text
        review_title = response.css( 'span.noQuotes::text')
        # extract and clean the review title text
        review_title = review_title.extract_first()
        #review date
        review_date=response.css('span.ratingDate::text').extract_first()
        # direct to review text
        review_text = response.css('p.partial_entry::text')
        # extract and clean review text
        review_text = review_text.extract_first()
        # store this in dictonary
        reviews_list.append([response.url, review_title, review_date, review_text])


# Initialize the list
reviews_list=[]
import csv

#
# Run the Spider
process = CrawlerProcess()
process.crawl(TASpider)
process.start()

# reviews_list=list(set(reviews_list))
print(len(reviews_list))
print(reviews_list[-4:])

with open('reviewsData.csv', 'w') as f:
    #configure writer to write standard csv file
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Site', 'Review_title', 'Review_date', 'Review_paragraph'])
    for item in reviews_list:
        #Write item to f
        writer.writerow([item[0], item[1], item[2], item[3]]) 