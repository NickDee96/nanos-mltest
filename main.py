import requests as req
from bs4 import BeautifulSoup as soup
from gensim.models import Word2Vec
from gensim.models.keyedvectors import Word2VecKeyedVectors
from selenium import webdriver
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
from selenium.webdriver.firefox.options import Options
import joblib
from nltk.stem import WordNetLemmatizer 
import sys 
import platform
from sklearn.decomposition import PCA
import plotly.graph_objects as go  



nltk.download('stopwords')
nltk.download('wordnet')
global lemmatizer, model
lemmatizer = WordNetLemmatizer()
model = joblib.load("model/wiki_pretrained_model.pkl")




def get_text(url):
    try:
        page = soup(req.get(url).text,"lxml")
    except req.exceptions.SSLError:
        if platform.system() == 'Windows':
            driver_path = 'geckodriver/geckodriver.exe'
        elif platform.system() == 'Linux':
            driver_path = 'geckodriver/geckodriver'
        options = Options()
        options.headless = True
        driver=webdriver.Firefox(executable_path = driver_path,options=options)
        driver.get(url)
        page = soup(driver.page_source,"lxml")
    return page.text







def process_text(text):
    st_words = list(stopwords.words("english"))
    text = re.sub(r"\d+", " ", text).strip()
    text = text.replace("\xa0"," ")
    text = re.sub(r'[^\w\s]',' ',text).lower()
    text_list = [lemmatizer.lemmatize(x.strip()) for x in text.split() if x.strip() not in st_words]
    if len(text_list) == 0:
        print("Loading Website Failed")
        return None
    else:
        return  set(text_list)




def match(text_list,search_words):
    similar_words = []
    phrase_vec_list = []
    for search_word in search_words:
        phrase_list = []
        for word in search_word.split():
            vec = model[word.lower()]
            phrase_list.append(vec)
            
        phrase_vec = sum(phrase_list)/len(search_word.split())
        phrase_vec_list.append(phrase_vec)

        words = []
        for word in text_list:
            try:
                w_vector  = model[word]
                words.append(word)
            except KeyError:
                pass

        distances = model.distances(phrase_vec,words)
        sort_index = [int(x) for x in np.argsort(distances)]

        similar_words += [words[x] for x in sort_index[:10]]
    similar_words = set(similar_words)

    sm_vec = np.array([model[x] for x in similar_words])
    phrase_vec_np = np.array(phrase_vec_list)
    
    pca = PCA(n_components=3)
    pca.fit(sm_vec)
    sm_pca = pca.transform(sm_vec)
    pv_pca = pca.transform(phrase_vec_np)
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x = sm_pca[:,0],
            y = sm_pca[:,1],
            z = sm_pca[:,2],
            mode = "markers+text", 
            text = list(similar_words),
            hoverinfo="text",
            name = "Similar Words in the text",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x = pv_pca[:,0],
            y = pv_pca[:,1],
            z = pv_pca[:,2],
            mode = "markers+text", 
            text = list(search_words),
            hoverinfo="text",
            name = "Search Words",
            marker=dict(
                color='rgba(0, 220, 250, 0.8)',
                size=20,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
        )
    )
    fig.update_layout(
        title = "A spatial representation of the distances between the Products/Services and similar words in the text"
    )


    return similar_words,fig



def main_func(url,search_words):
    text = get_text(url)
    text_list = process_text(text)
    similar_words = match(text_list,search_words)
    return similar_words



if __name__ == "__main__":
    url = sys.argv[1]
    search_words = [x.strip().replace("_"," ") for x in sys.argv[2].split(",")]
    print(main_func(url,search_words))



