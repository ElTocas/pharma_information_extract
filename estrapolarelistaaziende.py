# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:39:29 2021

@author: marti
"""

import pandas as pd
import numpy as np


import streamlit as st
import streamlit_tags
import plotly.express as px
#import plotly.figure_factory as ff

@st.cache(allow_output_mutation=True)
def persistdata():
    return {}

Tab_aifa = persistdata()
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

# creo dizionario aziende
dizionario = dict()

for azienda in aziende:
    temp = Tab_aifa_red[Tab_aifa_red["Titolare AIC"] == azienda]
    dizionario[azienda]=temp

dizionario_erog = dict()

for azienda in aziende:
    temp = Tab_aifa_red[Tab_aifa_red["Titolare AIC"] == azienda]
    denominazione=temp["Denominazione e Confezione"].str.lower()
    indice=np.where(denominazione.str.contains('erog'))
    temp = temp.iloc[indice[0],:]

dizionario_erog[azienda]=temp
  

## Visualizzazione





st.title('Esplora dataset AIFA (Classe A - per principio attivo) al 15-12-2020)')
st.subheader('by Tommaso Martire (to.martire@gmail.com)')


st.header('Dataframe content:')
st.dataframe(Tab_aifa.head(10))

st.header('Data info:')
st.write(Tab_aifa.shape[0].__str__() + ' rows,  ' + Tab_aifa.shape[1].__str__() + ' columns')
st.write(Tab_aifa.describe(include='object'))

# creo lista di suggerimenti
lista_suggerimenti_principio_attivo = Tab_aifa["Principio Attivo"].str.lower().astype(str).tolist()
Principi_attivi_selezionati = streamlit_tags.st_tags(
    label='# Inserisci principio attivo:',
    text='Press enter to add more',
    value=[],
    suggestions=lista_suggerimenti_principio_attivo,
    maxtags = 10,
    key='1')

if not Principi_attivi_selezionati:
    Principi_attivi_selezionati=lista_suggerimenti_principio_attivo



lista_suggerimenti_modalita_duso=Tab_aifa["Descrizione Gruppo Equivalenza"].str.lower().astype(str).tolist()
lista_uso=list()

for frase in lista_suggerimenti_modalita_duso:
    res = frase.split()
    try:
        indice_uso=res.index('uso')
        lista_uso.append(res[indice_uso+1])
    except:
        lista_uso.append("sconosciuta")

Tab_aifa_temp = persistdata()

        
Tab_aifa["modalità d'uso"]=lista_uso


lista_scelte_possibile_uso=np.array(['tutti'])


indice=np.where(principio_attivo.isin(Principi_attivi_selezionati))
Tab_aifa_temp = Tab_aifa.iloc[indice[0],:]

lista_scelte_possibile_uso=np.append(lista_scelte_possibile_uso,Tab_aifa_temp["modalità d'uso"].unique().astype(str))

moddalita_duso_selezionati = st.selectbox('Which use do u prefer?',lista_scelte_possibile_uso,index=0)



if moddalita_duso_selezionati=="tutti":
    moddalita_duso_selezionati=lista_uso
else:
    moddalita_duso_selezionati=[moddalita_duso_selezionati]



Tab_aifa_sel = persistdata()

if st.checkbox('Show results'):
    # Seleziono dati per grafico : popolo Ta_aifa_red
    indice=np.where(principio_attivo.isin(Principi_attivi_selezionati))
    Tab_aifa_sel = persistdata()
    Tab_aifa_sel = Tab_aifa.iloc[indice[0],:]
        
    denominazione=Tab_aifa_sel["modalità d'uso"].str.lower()
    indice=np.where(denominazione.isin(moddalita_duso_selezionati))
    Tab_aifa_sel = Tab_aifa_sel.iloc[indice[0],:]
    
    prodotto_per_azienda = Tab_aifa_sel.groupby(['Titolare AIC']).size()

    fig = fig = px.histogram(Tab_aifa_sel, x="Titolare AIC",labels={'x':'Nome Aziende', 'count':'Numero Confezioni'})
    st.plotly_chart(fig)

    

