import streamlit as st
import pandas as pd
import json
import requests
from datetime import date
from PIL import Image

st.title("News Express")

pesquisa_realizada = False

def var_glob ():
    
    global search
    search = None

    global language_options
    language_options = None

    global category_options
    category_options =  None

    global data_pesquisa
    data_pesquisa = None

    global country
    country = None

    global limite
    limite = None

    global my_offset
    my_offset = None

    global Source
    Source = None  

var_glob()

def pagina_inicial():
    
    

    st.subheader("Pesquise notícias em mais de 7 mil canais de comunicação nacionais e internacionais. ")

    st.subheader("Selecione os critérios de busca no menu lateral e pesquise!!")

    image = Image.open("News_sources.PNG")

    st.image(image, caption='By Mateus Alves - mateusnazareth85@gmail.com', output_format='PNG')

  
def carregar_dados():
    
    my_key = 'dee44a11f4481f96be4da6a4f3787842'

    params = dict(access_key = my_key, 
                keywords=search,
                languages=language_options,
                limit=limite,
                offset=my_offset,
                sources=Source,
                categories=category_options,
                countries=country,
                date=data_pesquisa,
                sort="published_desc",
                )

    res = requests.get('http://api.mediastack.com/v1/news', params=params)

    data = json.loads(res.text)

    global df

    df = pd.DataFrame(data['data'])

    df['published_at'] = pd.to_datetime(df['published_at']) 

def printar_noticias():
    i = 0
    for new in df:
        st.write ('Fonte:  ' + df.source[i].capitalize() + '\n')
        st.write (df.published_at[i] )
        st.subheader ('\n' + df.title[i] +'\n')
        st.caption (df.description[i] + '\n') 
        st.write ('link: ' + df.url[i] + '\n')
        #st.write (df.language[i] + '\n')   

        st.write('-------------------------------------------')
        i +=1
    
with st.sidebar:
    st.sidebar.header("Filtros")
    st.subheader("Selecione os filtros desejados")
    data_inicial = st.date_input("Data Inicial", date.today(), key="inicial")
    data_final = st.date_input("Data Final", date.today(), key="final")
    data_pesquisa = data_inicial, data_final 
    search = st.text_input('Palavra Chave',  key="se")
    language_options = st.multiselect(
     'Select the language',
     ['English', 'Portuguese', 'French', 'Italian', 'Dutch', 'Russian', 'Chinese'], ['Portuguese'],
      key="lang")

    for i in language_options:
        list=[]

        if i == "English":
           list.append ('en')

        elif i == "Portuguese":
            list.append('pt')

        elif i == "French":
           list.append ('fr')

        elif i == "Italian":
            list.append('it')

        elif i == "Dutch":
           list.append ('nl')

        elif i == "Russian":
            list.append('ru')

        elif i == "Chinese":
            list.append('zh')     

    language_options = list

# st.multiselect(
# 'Select the Category',
# ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology'])

def atualiza_params():   # Pega os inputs do Usuário
    global search_c
    global language_options_c    

    my_key = 'dee44a11f4481f96be4da6a4f3787842'

    params = dict(access_key = my_key, 
                keywords=search_c,
                languages=language_options_c,
                limit=limite,
                offset=my_offset,
                sources=Source,
                categories=category_options,
                countries=country,
                date=data_pesquisa,
                sort="published_desc",
                )

    res = requests.get('http://api.mediastack.com/v1/news', params=params)

    data = json.loads(res.text)

    global df

    df = pd.DataFrame(data['data'])

    df['published_at'] = pd.to_datetime(df['published_at']) 

with st.sidebar:
    result = st.button('Pesquisar')
   
if result:
    if search == "" :      
        st.warning('Informe a palavra chave ')
    else:
        # Variables edited 
        pesquisa_realizada = True
        data_pesquisa = data_inicial, data_final 
        search_c = search
        language_options_c = language_options
        # Variables non edited
        # limite = None
        # offset = None
        # sources = None
        # categories = None
        # countries = None
        
        carregar_dados()
        printar_noticias()
  
   
if pesquisa_realizada == False:
    pagina_inicial()
    
   
























