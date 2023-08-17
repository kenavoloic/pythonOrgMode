from bs4 import BeautifulSoup

import re
import requests

def bookScrap(article):
    image = article.find('img')
    title = image.attrs['alt']
    starTag = article.find('p')
    star = starTag['class'][1]
    price = article.find('p', class_='price_color').text
    price = float(price[1:])
    return [title, star, price]

def pageScrap(lien):
    requete = requests.get(lien)
    soupe = BeautifulSoup(requete.content, features='lxml')
    ol = soupe.find('ol')
    articles = ol.find_all('article', class_='product_pod')
    return articles

def nettoyageChaineHeure(chaine):
    """ format de la chaîne '12h 13' '0h47' par exemple. '12h 13' => '12h13' '0h47' => '0h47' """
    return re.sub('[^0-9|h]', '', chaine)

def conversionHeureMinutes(chaine):

    heure = nettoyageChaineHeure(chaine)
    # partition() contrairement à split() retourne toujours 3 parties
    duree = heure.partition('h')
    
    h = 0 if not bool(duree[0]) else duree[0]
    m = 0 if not bool(duree[2]) else duree[2]
    dureeMinutes = int(h)*60 + int(m)
    return (str(h).zfill(2) + 'h' +  str(m).zfill(2), dureeMinutes)


def imdb(film):
    """ contenu d'une balise contenant toutes les données relatives au film, en l'occurence, le top 250."""
    _titre = film.find('h3')
    decoupe = _titre.text.split('.')
    classement = decoupe[0]
    titre = decoupe[1].lstrip()
    meta = film.find_all('span', class_="cli-title-metadata-item")
    annee = meta[0].text
    duree = conversionHeureMinutes(meta[1].text)
    #duree = nettoyageChaineHeure(meta[1].text)
    pg = meta[2].text
    rating = film.find('span', attrs={'aria-label':True}, class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")
    
    return [int(classement), titre, int(annee), duree[0], duree[1], pg, float(rating.text.strip())]
