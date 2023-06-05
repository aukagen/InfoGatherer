from requests_html import HTMLSession
import pprint
from termcolor import colored
#import scrapy --> https://scrapeops.io/python-scrapy-playbook/scrapy-beginners-guide-user-agents-proxies/
    # https://scrapy.org/
from datetime import datetime
import pandas as pd
import numpy as np

#  <article class="news mx-auto bg-gray-700">



### Gathering the data ###
# Change next: add to a dictionary for neater printing?


class Gather:
    def __init__(self):
        #self.PAN_results = {}#{"Article#":{"Title":"", "URL":"", "kw_match":False,  "Summary":""}}
        #self.TM_result = {}
        self.keywords_list = ["malware", "threats", "threat", "AI", "ghat-gpt", "attack", "attacks", "ransomware"]

    def gather(self, url, xpath, header_xpath, url_xpath, extra_url):
        resultslist = {}
        session = HTMLSession()
        result = session.get(url)
        headings = result.html.xpath(xpath)

        count = 0
        for header in headings:
            count += 1
            resultslist[f"Article{count}"] = {"Title":"", "URL":"", "kw_match":False}#, "Summary":""}#
            header_txt = header.xpath(header_xpath)
            article_url = header.xpath(url_xpath)
            resultslist[f"Article{count}"]["Title"] = header_txt[0]
            if "https" in article_url[0]:
                resultslist[f"Article{count}"]["URL"] = article_url[0]
            else:
                #print("LINK: ", extra_url + article_url[0])    # REMOVE
                resultslist[f"Article{count}"]["URL"] = extra_url + article_url[0]

            for kw in self.keywords_list:
                if kw.lower() in header_txt[0].lower():
                    resultslist[f"Article{count}"]["kw_match"] = True
        
        return resultslist





class Sources:
    def __init__(self):
        pass
    def PAN(self):    # Unit42 PaloAltoNetworks
        research_url = "https://unit42.paloaltonetworks.com/latest-research/"
        xpath =  "//main//div[@class='grid row align-items-sm-start pb-40']//div/h3/a"
        header_xpath = "a[@data-page-track-value]/text()"
        url_xpath = "a/@href"

        reslist = Gather().gather(research_url, xpath, header_xpath, url_xpath, "")
        return reslist

    
    def TM(self):    # TrendMicro
        news_url = "https://www.trendmicro.com/vinfo/us/security/news/"
        extra_url = "https://www.trendmicro.com"
        xpath = "//main/div/div/section[2]/div/div/div/div/section[2]/div[2]/ul/*"
        header_xpath = '//li/div/div[@class="titlelist"]/h3/a/text()'
        url_xpath = '//li/div[@class="enclose"]/a/@href'
        

        reslist = Gather().gather(news_url, xpath, header_xpath, url_xpath, extra_url)
        return reslist
        
        
        


class Main:
    def __init__(self):
        #self.PAN_res = Sources().PAN()
        #self.TM_res = Sources().TM()
        pass
    '''
    def printing(self, dictionary):
        #Print headers too, to categorise the source of where the research/news is taken from...
        obj = dictionary #Sources().PAN()
        for i in range(1, len(obj)):
            if obj[f"Article{i}"]["kw_match"] == True:
                print(colored(f"MATCH: {obj[f'Article{i}']}", 'red'))
            else:
                print(obj[f'Article{i}'])
        #pprint.pprint(PAN_obj)
    '''

    def neat_printing(self, dictionary):
        #pd.set_option('display.max_rows', 9)
        pd.set_option('display.max_columns', 15)
        pd.set_option('display.max_colwidth', 200)
        #data = pd.DataFrame(dictionary)
        data = pd.DataFrame.from_dict(dictionary, orient="columns")
        
        #print(a(dictionary))
        data.style.applymap(self.highlight, colour="red")
        #data.style.applymap(self.highlight, dict=dictionary)
        print(data)
        
       
    def highlight(self, colour):
        #matches = []
        return f"color: {colour}" if v == True else None
        '''
        for article in dict:
            print(article)
            if dict[article]["kw_match"] == True:
                print("MATCH")
                color = "red"
                return 'background-color: %s' % color
                #matches.append(dict[article])
        '''
        #return ['background-color: yellow' for match in matches]
        #return 'background-color: %s' % color



    def main(self):
        #self.printing(Sources().PAN())
        #self.printing(Sources().TM())
        self.neat_printing(Sources().TM())
        self.neat_printing(Sources().PAN())

### Printing all the information neatly ###
# Use a terminal GUI for this / tables

if __name__ == "__main__":
    Main().main()
    
    #print(datetime.now().strftime())
    
    
    #Gather().gather("https://unit42.paloaltonetworks.com/latest-research/", "//main//div[@class='grid row align-items-sm-start pb-40']//div/h3/a", "a[@data-page-track-value]/text()", "a/@href", {})