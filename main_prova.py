# -*- coding: utf-8 -*-
"""
Created on Mon May 17 23:10:34 2021

@author: Tommaso
"""
from bs4 import BeautifulSoup
import requests
import it_core_news_sm
import numpy as np
import pandas as pd
import spacy



url = 'https://www.chiesi.com/air/'

r = requests.get(url)

data = r.text
soup = BeautifulSoup(data, 'html.parser')

desc = soup.find("div",attrs= {'class':"descrizioneareainterna"})  
desc_testo = desc.text
desc_testo

nlp=it_core_news_sm.load()


## Analisi prodotti registrati

doc = nlp(desc_testo)
# Create list of word tokens
token_list_testo = []


for token in doc:
    token_list_testo.append(token.text)
testo_numpy=np.array(token_list_testo)
dove_reserved=np.where(testo_numpy=='®')
dove_reserved=dove_reserved[0]-1

prodotti_registrati=testo_numpy[dove_reserved]
prodotti_registrati=np.unique(prodotti_registrati)    
token_list_sent_start=[]
for token in doc:
    token_list_sent_start.append(token.is_sent_start)    
    
vet_start_sent = np.where(token_list_sent_start)
vet_start_sent=vet_start_sent[0]
vet_stop_sent = vet_start_sent-1


indice_frasi_da_salvare=[]
frasi_da_salvare=[]
for i in range(len(vet_start_sent)-1):
    
    frase= token_list_testo[vet_start_sent[i] : vet_start_sent[i+1]]
    
    cistanno=pd.Series(prodotti_registrati).isin(frase).any()

    if cistanno:
        frase = " ".join(frase)
        frase = nlp(frase)
        #spacy.displacy.serve(frase, style="dep")
        indice_frasi_da_salvare.append(i)
        frasi_da_salvare.append(frase)
        
#spacy.displacy.serve(frasi_da_salvare, style="ent")


fraseesempio=frasi_da_salvare[2]
#spacy.displacy.serve(fraseesempio, style="dep")

for token in fraseesempio:
    print(token.lemma_)



    
    

    
###### PROVO NLTK

#from nltk.tokenize import sent_tokenize

# divido in frasi
#sentence_tokenizer_output = sent_tokenize(desc_testo)






#import spacy

 #print([(w.text, w.pos_) for w in doc])
 
# print([(w.pos_) for w in doc])

#for ent in doc.ents:
#    print(ent.text, ent.label_)
#from pathlib import Path
#svg = displacy.render(doc, style="dep")
##output_path = Path("sentence.svg")
#output_path.open("w", encoding="utf-8").write(svg)

#Streamlit provare []