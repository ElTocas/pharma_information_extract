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

# Seleziono più principi attivi
Principi_attivi_selezionati = streamlit_tags.st_tags(
    label='# Inserisci principio attivo:',
    text='Press enter to add more',
    value=[],
    suggestions=Tab_aifa["Principio Attivo"].str.lower().astype(str).tolist(),# creo lista di suggerimenti
    maxtags = 10,
    key='1')
if not Principi_attivi_selezionati:
    Principi_attivi_selezionati=Tab_aifa["Principio Attivo"].str.lower().astype(str).tolist()


# Aggiungo la colonna modalità d'uso
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

# Aggiungo check selezione modalità d'uso
lista_scelte_possibile_uso=np.array(['tutti'])
indice=np.where(principio_attivo.isin(Principi_attivi_selezionati))
Tab_aifa_temp = Tab_aifa.iloc[indice[0],:]
lista_scelte_possibile_uso=np.append(lista_scelte_possibile_uso,Tab_aifa_temp["modalità d'uso"].unique().astype(str))
moddalita_duso_selezionati = st.selectbox("Selezionare la modalità d'uso specifica",
                                          lista_scelte_possibile_uso,
                                          index=0)
if moddalita_duso_selezionati=="tutti":
    moddalita_duso_selezionati=lista_uso
else:
    moddalita_duso_selezionati=[moddalita_duso_selezionati]

# Aggiungo nome farmaco
lista_suggerimenti_nome_farmaco=Tab_aifa["Denominazione e Confezione"].str.lower().astype(str).tolist()
lista_nomef=list()
for frase in lista_suggerimenti_nome_farmaco:
    try:
        indice_nomef=frase.index('*')
        lista_nomef.append(frase[0:indice_nomef])
    except:
        lista_nomef.append("sconosciuta")

Tab_aifa["nomefarmaco"]=lista_nomef

indice=np.where(principio_attivo.isin(Principi_attivi_selezionati))
Tab_aifa_temp = Tab_aifa.iloc[indice[0],:]
indice=np.where(Tab_aifa_temp["modalità d'uso"].isin(moddalita_duso_selezionati))
Tab_aifa_temp = Tab_aifa_temp.iloc[indice[0],:]

        
lista_scelte_possibile_nomefarmaco=np.array(['tutti'])
lista_scelte_possibile_nomefarmaco=np.append(lista_scelte_possibile_nomefarmaco,np.unique(Tab_aifa_temp["nomefarmaco"].astype(str)))

farmaco_selezionati = st.selectbox("Selezionare il nome del farmaco specifico",
                                          lista_scelte_possibile_nomefarmaco,
                                          index=0)
if farmaco_selezionati=="tutti":
    farmaco_selezionati=lista_scelte_possibile_nomefarmaco
else:
    farmaco_selezionati=[farmaco_selezionati]





if st.checkbox('Mostra risultati'):
    # Seleziono dati per grafico
    
    #seleziono per principio attivo
    indice=np.where(principio_attivo.isin(Principi_attivi_selezionati))
    Tab_aifa_sel = Tab_aifa.iloc[indice[0],:]
    #seleziono per modalita duso    
    denominazione=Tab_aifa_sel["modalità d'uso"].str.lower()
    indice=np.where(denominazione.isin(moddalita_duso_selezionati))
    Tab_aifa_sel = Tab_aifa_sel.iloc[indice[0],:]
    #seleziono per farmaco
    nomefarmaco=Tab_aifa_sel["nomefarmaco"].str.lower()
    indice=np.where(nomefarmaco.isin(farmaco_selezionati))
    Tab_aifa_sel = Tab_aifa_sel.iloc[indice[0],:]
    
    
    
    num_prodotti_per_azienda = Tab_aifa_sel.groupby(['Titolare AIC']).size()
    
    # else:
        
        
    fig = px.histogram(Tab_aifa_sel, 
                       x="Titolare AIC",
                       color="Principio Attivo",
                       color_discrete_sequence=px.colors.qualitative.Light24,
                       hover_data=['nomefarmaco','Principio Attivo'])
    st.plotly_chart(fig)
        
        
        
    
    
    
    
    
    
    if st.checkbox('Mostra DataFrame informazioni aggiuntive'):
        Tab_aifa_selA=Tab_aifa_sel;
        
        Aziende_selezionate = streamlit_tags.st_tags(
            label='# Inserisci azienda:',
            text='Press enter to add more',
            value=[],
            suggestions=Tab_aifa_selA["Titolare AIC"].str.lower().astype(str).tolist(),# creo lista di suggerimenti
            maxtags = 10)
    
        if not Aziende_selezionate:
            Aziende_selezionate=Tab_aifa_selA["Titolare AIC"].str.lower().astype(str).tolist()
       
        
        temp_az=Tab_aifa_selA["Titolare AIC"].str.lower()
        indice=np.where(temp_az.isin(Aziende_selezionate))
        Tab_aifa_selA = Tab_aifa_selA.iloc[indice[0],:]
        
        nummeri=list()
        for elem in Tab_aifa_selA['Prezzo al pubblico �']:
            try:
                elemento=elem.replace(",",".")
                nummeri.append(float(elemento))
            except:
                nummeri.append(float("NAN"))   
        
        Tab_aifa_selA["prezzoalpubblico"]=nummeri
        
        
        Tab_aifa_sel_nomefarmaco = Tab_aifa_selA.groupby(['nomefarmaco','Titolare AIC'])[["prezzoalpubblico"]].mean()
        
        st.text("Tabella ridotta per nome commerciale farmaco venduto e media")
        st.dataframe(data=Tab_aifa_sel_nomefarmaco)
    
        user_input = st.text_input("Inserire una stringa della parola che si vuole trovare", 'erog')
        colonna_selezionata = st.selectbox("Selezionare il nome di una colonna in cui cercare",
                                          Tab_aifa_selA.columns,
                                          index=2)
        try:
            if st.checkbox('Cerca parola'): 
                Tab_aifa_selA['parolacercataindec'] = Tab_aifa_selA[colonna_selezionata].str.find(user_input)
                Tab_aifa_selA=Tab_aifa_selA.loc[Tab_aifa_selA['parolacercataindec']>-1]
                fig = px.histogram(Tab_aifa_selA, 
                                   x="Titolare AIC",
                                   color="Principio Attivo",
                                   color_discrete_sequence=px.colors.qualitative.Light24,
                                   hover_data=['nomefarmaco','Principio Attivo'])
                st.plotly_chart(fig)
                st.dataframe(data=Tab_aifa_selA)    
                fig2 = px.histogram(Tab_aifa_selA, 
                                   x="Titolare AIC",
                                   y="prezzoalpubblico",
                                   color="Principio Attivo",
                                   color_discrete_sequence=px.colors.qualitative.Light24,
                                   hover_data=['nomefarmaco','Principio Attivo'])
                st.plotly_chart(fig2)
                
        except:
            st.text("Parola non trovata nella colonna scelta")
            
            st.plotly_chart(fig)
            st.dataframe(data=Tab_aifa_selA) 
            
            