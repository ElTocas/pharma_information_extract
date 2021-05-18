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
# Create list of word tokens
token_list = []
for token in doc:
    token_list.append(token.text)
    token_list.append(token.lemma)
print(token_list)

sentence_spans = list(doc.sents)

for token in sentence_spans:
    print(token.text)





from spacy import displacy

 #print([(w.text, w.pos_) for w in doc])
 
# print([(w.pos_) for w in doc])

#for ent in doc.ents:
#    print(ent.text, ent.label_)
#from pathlib import Path
#svg = displacy.render(doc, style="dep")
##output_path = Path("sentence.svg")
output_path.open("w", encoding="utf-8").write(svg)

#Streamlit provare []