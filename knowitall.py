"""
En gpt AI crawler som söker igenom vetenskapliga artiklar och summerar dom,
dra slutsatser, intressanta vetenskapliga concept, programmering, etc
"""

from openai import OpenAI
from scholarly import scholarly
from bs4 import BeautifulSoup
from selenium import webdriver
import json

class Crawler():
    def __init__(self, apikey: str, save_output=False):
        self._apikey=apikey
        self._save_output = save_output
        self.output_to_save = {}
    def _crawl_topic(self, topic):
        query = scholarly.search_pubs(topic)
        data = next(query)
        if self._save_output:
            self.output_to_save.update({"tag":f"{len(self.output_to_save)}"}) 
        return data['pub_url']                 
    def _get_pdf(self, gpt_input):
        url = self._crawl_topic(gpt_input)
        dr = webdriver.Chrome()
        dr.get(url)
        soup = BeautifulSoup(dr.page_source, 'lxml')
        if self._save_output:
            self.output_to_save.update({'url':url})
        return soup.get_text()
    
    def search_and_summarise(self, topic: str):
        text = self._get_pdf(topic)
        client = OpenAI(api_key=self._apikey)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarise this text {text}",
                }
            ],
            model="gpt-4",
        ) 
        msg = chat_completion.choices[0].message.content
        if self._save_output:
            self.output_to_save.update({"content": msg})
        return msg
    
    def run(self):
        client = OpenAI(api_key=self._apikey)
        while(True):
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"You are an AI, that comes up with a topic for research, in the STEM field, physics, AI, computer sciene, math, Engineering",
                    }
                ],
                model="gpt-4",
            )      
            msg = chat_completion.choices[0].message.content
            self.summarise(msg)
            self.write_to_file()
    
    def write_to_file(self):
        with open(self.output_to_save["tag"], "w+") as file:
            file.write(json.dumps(self.output_to_save))
        
        