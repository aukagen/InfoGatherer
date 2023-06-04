from requests_html import HTMLSession
import pprint
from termcolor import colored
#import scrapy --> https://scrapeops.io/python-scrapy-playbook/scrapy-beginners-guide-user-agents-proxies/
    # https://scrapy.org/

### Common variables ###


### For PAN - Unit42 ###
"""
class Websites:
    def __init__(self):
        pass
    def PAN(self):
        research_url = "https://unit42.paloaltonetworks.com/latest-research/"
        session = HTMLSession()
        return session.get(research_url)
"""


#  <article class="news mx-auto bg-gray-700">



### Gathering the data ###
# Change next: add to a dictionary for neater printing?


class Gather:
    def __init__(self):
        self.PAN_results = {}#{"Article#":{"Title":"", "URL":"", "kw_match":False,  "Summary":""}}
        self.keywords_list = ["malware", "threats", "threat", "AI", "ghat-gpt", "attack", "attacks", "ransomware"]

    def PAN(self):
        research_url = "https://unit42.paloaltonetworks.com/latest-research/"
        session = HTMLSession()
        PAN_r = session.get(research_url)
        headings = PAN_r.html.xpath("//main//div[@class='grid row align-items-sm-start pb-40']//div/h3/a")

        count = 0
        for header in headings:
            count += 1
            self.PAN_results[f"Article{count}"] = {"Title":"", "URL":"", "kw_match":False, "Summary":""}
            header_txt = header.xpath("a[@data-page-track-value]/text()")
            article_url = header.xpath("a/@href")
            self.PAN_results[f"Article{count}"]["Title"] = header_txt[0]
            self.PAN_results[f"Article{count}"]["URL"] = article_url[0]
            
            for kw in self.keywords_list:
                if kw.lower() in header_txt[0].lower():
                    self.PAN_results[f"Article{count}"]["kw_match"] = True
        
        return self.PAN_results
    
        
        


class Main:
    def __init__(self):
        pass
    def printing(self):
        PAN_obj = Gather().PAN()
        for i in range(1, len(PAN_obj)):
            if PAN_obj[f"Article{i}"]["kw_match"] == True:
                print(colored(f"MATCH: {PAN_obj[f'Article{i}']}", 'red'))
            else:
                print(PAN_obj[f'Article{i}'])
        #pprint.pprint(PAN_obj)
### Printing all the information neatly ###
# Use a terminal GUI for this / tables

if __name__ == "__main__":
    Main().printing()
    #Gather().PAN()