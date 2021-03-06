# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:39:29 2021

Estrapolazione dati riguardanti farmaci commerciali e aziende, riconducibili a:
    principio attivo/i
    modalità d'uso
    Aziende specifica
    Parola specifica ll'interno di una colonna
    
Il File usato come input è quello dell'AIFA'

@author: eltocas
"""

import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
import plotly.express as px
#import plotly.figure_factory as ff

@st.cache(allow_output_mutation=True)
def persistdata():
    return {}

## Miglioro la tabella ed aggiungo campi
Tab_aifa = pd.read_csv('Classe_A.csv',sep='\t')
principio_attivo=Tab_aifa["Principio Attivo"].str.lower()
# sostituisco i nan con un valore stringa
Tab_aifa["Solo in lista di Regione:"]=Tab_aifa["Solo in lista di Regione:"].fillna("non disponibile")
# aggiungo prezzo al pubblico
nummeri=list()
for elem in Tab_aifa['Prezzo al pubblico �']:
    try:
        elemento=elem.replace(",",".")
        nummeri.append(float(elemento))
    except:
        nummeri.append(float("NAN"))   
        
Tab_aifa["prezzoalpubblico"]=nummeri
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

Tab_aifa["modalità d'uso"]=lista_uso

## Visualizzazione


title_container = st.beta_container()
col1, col2 = st.beta_columns([3, 7])
image = Image.open('./pharmaopen.png')
with title_container:
    with col1:
        st.image(image,width=150)
    with col2:
        st.title('Esplora [dataset AIFA] (https://www.aifa.gov.it/liste-dei-farmaci) (Classe A - per principio attivo) al 15-12-2020')
        st.subheader('by Tommaso Martire')


st.header('Esempio del contenuto della tabella con alcune colonne estrapolate:')
st.dataframe(Tab_aifa.head(2))
st.header('Informazioni aggiuntine:')
st.write(Tab_aifa.shape[0].__str__() + ' numero farmaci considerati,  ' + Tab_aifa.shape[1].__str__() + ' numero variabili considerate')
st.write(Tab_aifa.describe(include='object'))

st.title("Obiettivo")
st.write("L'obiettivo della dashboard è quello di visualizzare le informazioni riguardo le aziende che commercializzano il principio attivo selezionato")
st.write("Esempio: selezionando i principi attivi utilizzati nella cura della BPCO: fluticasone, beclometasone, budesonide la dashboard restituirà le aziende che producono questi principi attivi")

# Seleziono più principi attivi
## nn uso multiselect eprchè lento


Principi_attivi_selezionati = st.multiselect(
    label='Inserisci uno (o più) principio attivo da alizzare:',
    options = ["tutti"] + Tab_aifa["Principio Attivo"].str.lower().unique().astype(str).tolist(),
    default = ["tutti"],
    help="inserisci il principio attivo con tutte le lettere minuscole e segui i suggerimenti"
)

if Principi_attivi_selezionati==["tutti"]:
    Principi_attivi_selezionati = Tab_aifa["Principio Attivo"].str.lower().unique().astype(str).tolist()

#Principi_attivi_selezionati = streamlit_tags.st_tags(
#    label='# Inserisci principio attivo:',
#    text='Press enter to add more',
#    value=[],
#    suggestions=Tab_aifa["Principio Attivo"].str.lower().astype(str).tolist(),# creo lista di suggerimenti
#    maxtags = 10,
#    key='1')
#if not Principi_attivi_selezionati:
#    Principi_attivi_selezionati=Tab_aifa["Principio Attivo"].str.lower().astype(str).tolist()


# Aggiungo check selezione modalità d'uso singola

lista_scelte_possibile_uso=np.array(['tutti'])
indice=np.where(principio_attivo.isin(pd.Series(Principi_attivi_selezionati)))
Tab_aifa_temp = Tab_aifa.iloc[indice[0],:]
lista_scelte_possibile_uso=np.append(lista_scelte_possibile_uso,Tab_aifa_temp["modalità d'uso"].unique().astype(str)).tolist()
#moddalita_duso_selezionati = st.selectbox("Selezionare la modalità d'uso specifica",
#                                          lista_scelte_possibile_uso,
#                                          index=0)

# Aggiungo check selezione modalità d'uso multipla
#moddalita_duso_selezionati=Tab_aifa["modalità d'uso"].str.lower().astype(str).unique().tolist()
#moddalita_duso_selezionati=st.multiselect("Seleziona uno o più modalità d'uso", Tab_aifa["modalità d'uso"].str.lower().astype(str).unique(),Tab_aifa["modalità d'uso"].str.lower().astype(str).unique())
moddalita_duso_selezionati = st.multiselect(
    label="Inserisci la modalità d'uso da selezionare:",
    options = lista_scelte_possibile_uso,
    default = ["tutti"],
    help="inserisci una o più modalità d'uso da selezionare"
)

if moddalita_duso_selezionati==["tutti"]:
    moddalita_duso_selezionati = Tab_aifa_temp["modalità d'uso"].str.lower().unique().astype(str).tolist()
#moddalita_duso_selezionati = streamlit_tags.st_tags(
#     label="# Inserisci la modalità d'uso da selezionare:",
#     text='Press enter to add more',
#     value=[],
#     suggestions=Tab_aifa["modalità d'uso"].str.lower().astype(str).tolist(),# creo lista di suggerimenti
#     maxtags = 10,
#     key='11')


#if not moddalita_duso_selezionati:
#     moddalita_duso_selezionati=Tab_aifa["modalità d'uso"].str.lower().astype(str).tolist()



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
    indice=np.where(principio_attivo.isin(pd.Series(Principi_attivi_selezionati)))
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
    datidavisualizzare=["Denominazione e Confezione","nomefarmaco","Principio Attivo","modalità d'uso","prezzoalpubblico","Solo in lista di Regione:"]    
        
        
    fig = px.bar(Tab_aifa_sel, 
                       x="Titolare AIC",
                       color="Principio Attivo",
                       color_discrete_sequence=px.colors.qualitative.Light24,
                       hover_data=datidavisualizzare)
    st.plotly_chart(fig)
        

    
    
    if st.checkbox('Mostra DataFrame informazioni aggiuntive'):
        Tab_aifa_selA=Tab_aifa_sel
        
        Aziende_selezionate = st.multiselect(
            label="Inserisci le aziende che vuoi selezionare:",
            options = ["tutte"] + Tab_aifa_selA["Titolare AIC"].str.lower().unique().astype(str).tolist(),
            default = ["tutte"],
            help="inserisci una o più modalità d'uso da selezionare"
        )

        if Aziende_selezionate==["tutte"]:
            Aziende_selezionate = Tab_aifa_selA["Titolare AIC"].str.lower().unique().astype(str).tolist()

        #Aziende_selezionate = streamlit_tags.st_tags(
        #    label='Inserisci azienda:',
        #    text='Press enter to add more',
        #    value=[],
        #    suggestions=Tab_aifa_selA["Titolare AIC"].str.lower().astype(str).tolist(),# creo lista di suggerimenti
        #    maxtags = 10)
    
        #if not Aziende_selezionate:
        #    Aziende_selezionate=Tab_aifa_selA["Titolare AIC"].str.lower().astype(str).tolist()
       
        
        temp_az=Tab_aifa_selA["Titolare AIC"].str.lower()
        indice=np.where(temp_az.isin(Aziende_selezionate))
        Tab_aifa_selA = Tab_aifa_selA.iloc[indice[0],:]

        Tab_aifa_sel_nomefarmaco = Tab_aifa_selA.groupby(['nomefarmaco','Titolare AIC'])[["prezzoalpubblico"]].mean()
        

        st.text("Tabella ridotta per nome commerciale farmaco venduto e media prezzo delle diverse confezioni")
        st.dataframe(data=Tab_aifa_sel_nomefarmaco)
        fig = px.bar(Tab_aifa_selA, 
                    x="Titolare AIC",
                    color="Principio Attivo",
                    color_discrete_sequence=px.colors.qualitative.Light24,
                    hover_data=datidavisualizzare)
        st.plotly_chart(fig)

        ricerca_app_container = st.beta_container()  
        col1, col2 = st.beta_columns([5, 5])
        with ricerca_app_container:
            st.write("Analisi avanzata (ricerca parola in colonna)")
            with col1:
                user_input = st.text_input("Inserire una stringa della parola che si vuole trovare", 'erog')
            with col2:
                colonna_selezionata = st.selectbox("Selezionare il nome di una colonna in cui cercare",
                                          Tab_aifa_selA.columns,
                                          index=2)

        
        
        try:
            if st.checkbox('Cerca parola'): 
                Tab_aifa_selA['parolacercataindec'] = Tab_aifa_selA[colonna_selezionata].str.find(user_input)
                Tab_aifa_selA=Tab_aifa_selA.loc[Tab_aifa_selA['parolacercataindec']>-1]
                fig = px.bar(Tab_aifa_selA, 
                                   x="Titolare AIC",
                                   color="Principio Attivo",
                                   color_discrete_sequence=px.colors.qualitative.Light24,
                                   hover_data=datidavisualizzare)
                st.plotly_chart(fig)
                st.dataframe(data=Tab_aifa_selA)    
                
                
        except:
            st.text("Parola non trovata nella colonna scelta")
            
            