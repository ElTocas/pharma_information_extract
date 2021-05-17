# -*- coding: utf-8 -*-
"""
Created on Mon May 17 23:10:34 2021

@author: Tommaso
"""
from bs4 import BeautifulSoup
import requests
import it_core_news_sm


url = 'https://www.chiesi.com/air/'

r = requests.get(url)

data = r.text
soup = BeautifulSoup(data, 'html.parser')

desc = soup.find("div",attrs= {'class':"descrizioneareainterna"})  
desc_testo = desc.text
desc_testo

nlp=it_core_news_sm.load()


doc = nlp(desc_testo)

 print([(w.text, w.pos_) for w in doc])
 
 print([(w.pos_) for w in doc])
 