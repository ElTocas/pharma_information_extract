# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:39:29 2021

@author: marti
"""

import pandas as pd
import numpy as np

Tab_aifa = pd.read_csv('Classe_A.csv',sep='\t')

parola_da_cerca = "Ciclesonide";
#parole_da_cerca = pd.Series(["ciclesonide", "fluticasone","olodaterolo","tiotropio","formoterolo","beclometasone","budesonide","indacaterolo","glicopirronio","aclidinio","benlarizumab"]);

parole_da_cerca = pd.Series(["fluticasone", "beclometasone","budesonide"]);
principio_attivo=Tab_aifa["Principio Attivo"].str.lower()


indice=np.where(principio_attivo.isin(parole_da_cerca))

Tab_aifa_red = Tab_aifa.iloc[indice[0],:]

denominazione=Tab_aifa_red["Descrizione Gruppo Equivalenza"].str.lower()

indice=np.where(denominazione.str.contains('respiratorio'))

Tab_aifa_red = Tab_aifa_red.iloc[indice[0],:]



aziende = Tab_aifa_red["Titolare AIC"]
aziende = aziende.unique()


dizionario = dict()

for azienda in aziende:
    temp = Tab_aifa_red[Tab_aifa_red["Titolare AIC"] == azienda]
    dizionario[azienda]=temp


