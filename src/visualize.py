
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from scipy.ndimage import gaussian_gradient_magnitude
from PIL import Image

from src import retrieve


def plot_wordcloud(wordcloud):
    plt.figure(figsize=(20,20))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

def show_wordcloud(data, stopwords = None, title = None):
    text = data

    wordcloud = WordCloud(stopwords = stopwords,
                          collocations=False,
                          background_color='white').generate(text)

    plot_wordcloud(wordcloud, title)

def cria_imagem_nuvem(letra, url_capa, stop):
    
    letra = letra.lower()
    capa = retrieve.baixa_capa(url_capa, 'temp')
    
    mask = np.array(Image.open(capa))

    # Generate wordcloud
    wordcloud = WordCloud(width = 3000, 
                          height = 3000, 
                          random_state=1, 
                          background_color='black', 
                          colormap='rainbow', 
                          collocations=False, 
                          stopwords = stop,
                          mask=mask).generate(letra)
    # Plot
    plot_wordcloud(wordcloud)
    
def cria_nuvem_capa(letra, url_capa, stop):
    
    letra = letra.lower()
    try:
        capa = retrieve.baixa_capa(url_capa, 'temp')
        capa = retrieve.aumenta_imagem(capa)
        mask = np.array(Image.open(capa))
    except:
        capa = '../images/song.webp'
        capa = retrieve.aumenta_imagem(capa)
        mask = np.array(Image.open(capa))
    
    

    wordcloud = WordCloud(stopwords=stop, 
                              background_color="white", 
                              random_state = 24,
                              max_words=1000, 
                              mask=mask).generate(letra)

    # create coloring from image
    image_colors = ImageColorGenerator(mask)
    wordcloud.recolor(color_func=image_colors)

    plt.figure(figsize=[10,10])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # store to file
    #plt.savefig("img/spa_wine.png", format="png")
    
    #plt.show()