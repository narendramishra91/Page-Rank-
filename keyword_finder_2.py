import requests
from bs4 import BeautifulSoup
import pandas as pd
import operator 
from collections import Counter
import json 

class keyword_finder_class:
    
    not_keyword = list(pd.read_csv('mostFrequentWord.csv')['word'])
    
    def __init__(self, url):
        self.url = url
        self.source_code = requests.get(self.url).text
        self.soup = BeautifulSoup(self.source_code, 'html.parser')
        self.get_title = self.soup.find_all('title')
        self.get_body = self.soup.find_all('body')
        self.clean_body_list = []
        self.clean_title_list = []
        self.hyperlinks = [x for x in [a['href'] for a in self.soup.find_all('a', href=True) if a.text] if                     x.startswith('https') or x.startswith('http')]
    
   
    @staticmethod
    def get_list(contents):
        for each_text in contents:
            content = each_text.text
            word_list = content.lower().split()
            return word_list
        
        
    @staticmethod
    def clean_wordlist_special_symbol(wordlist): 
        
        clean_list =[] 
        for word in wordlist or []: 
            symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/., '
          
            for i in range (0, len(symbols)): 
                word = word.replace(symbols[i], '') 
              
            if len(word) > 0: 
                clean_list.append(word) 
        return clean_list 
    
    @classmethod
    def clean_wordlist_not_keyword(cls, word_list):
        clean_list = []
        for word in word_list:
            if word not in cls.not_keyword:
                clean_list.append(word)
                
        return clean_list
                

    def get_title_text_list(self):
        self.clean_title_list = self.clean_wordlist_not_keyword(self.clean_wordlist_special_symbol(self.get_list(self.get_title)))
        
    def get_body_text_list(self):
        self.clean_body_list = self.clean_wordlist_not_keyword(self.clean_wordlist_special_symbol(self.get_list(self.get_body)))

    def keywords(self, keyword):
        with open('sample.json', 'r+') as openfile:         
            json_object = json.load(openfile) 
            if keyword not in json_object:
                json_object[keyword] = [self.url]
            else:
                if self.url not in json_object[keyword]:
                    json_object[keyword].append(self.url)
            openfile.seek(0)
            json.dump(json_object, openfile, indent = 4)
            openfile.truncate()
        
        
    def create_dictionary(self):
        keywords_body = []
        word_count = {} 
        self.get_body_text_list()
        for word in self.clean_body_list: 
            if word in word_count: 
                word_count[word] += 1
            else: 
                word_count[word] = 1
              
        c = Counter(word_count) 
        top = c.most_common(5)
        for keyword in top:
            keywords_body.append(str(keyword[0]))
        return keywords_body
    
    def links_associated(self):
        with open('links.json', 'r+') as openfile:         
            json_object = json.load(openfile) 
            if self.url not in json_object:
                json_object[self.url] = self.hyperlinks
            openfile.seek(0)
            json.dump(json_object, openfile, indent = 4)
            openfile.truncate()
    
    def save_keyword(self):
        self.get_body_text_list()
        body_list = self.clean_body_list
        self.get_title_text_list()
        title_list = self.clean_title_list
        total_keyword = body_list + title_list
        print(total_keyword)
        for keyword in total_keyword:
            self.keywords(str(keyword))
        self.links_associated()