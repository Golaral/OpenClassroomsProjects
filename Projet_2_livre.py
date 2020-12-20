import requests
from bs4 import BeautifulSoup
import time
from sys import *
from math import *

links = []
informations = []

#activer pep8
#Recuperation des urls de tous les livres du site
def recuperation_url(): #save_urls
    for i in range(1, 51):
        response = requests.get(f'http://books.toscrape.com/catalogue/page-{i}.html')
        print(response)
        if response.ok:
            print('Page : ' + str(i))
            soup = BeautifulSoup(response.text, 'lxml')
            list_book_a = soup.findAll('article', {'class': 'product_pod'})
            for book_a in list_book_a: #soup.select("#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.image_container > a")
                #a = article.find('a')
                #link = a['href']
                links.append('http://books.toscrape.com/catalogue/' + link)
            time.sleep(3)
        else:
            print("Erreur lors de la recuperation des donnees.")
    with open('urls_all_books.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')
    return

#stockage du livre choisi ou des livres du site en entier en fonction du choix de l'utilisateur 
def stockage_info(livre, choix):
    reponse = requests.get(livre)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, 'lxml')
        tds = soup.find('table',{'class': 'table table-striped'}).findAll('tr')
        title = soup.find('h1').text
        categorie = soup.find('ul',{'class': 'breadcrumb'}).findAll('a')[2].text
        url_image = soup.select_one("#product_gallery > div > div > div > img")["src"]
        prix_ht = tds[2].text
        prix_it = tds[3].text
        upc = tds[0].text
        nombre_disponible = tds[5].text
        ratio_vues = tds[6].text
        informations = [title, categorie, url_image, upc, prix_ht, prix_it, nombre_disponible, ratio_vues]
        if choix == 1:
            with open('informations_du_livre.csv', 'w') as outf: #factorisation
                outf.write('Titre, Categorie, URL, UPC, Prix Hors Taxe, Prix Avec Taxe, Nombre Disponible, Ratio des Vues\n')
                outf.write(str(informations[0]) + ' , '.rstrip('\n') + str(informations[1]) + ' , '.rstrip('\n') + str(informations[2]) + ' , '.rstrip('\n') + str(informations[3]) + ' , '.rstrip('\n') + str(informations[4]) + ' , '.rstrip('\n') + str(informations[5]) + ' , '.rstrip('\n') + str(informations[6]) + ' , '.rstrip('\n') + str(informations[7]))
        elif choix == 2:
            with open('informations_des_livres.csv', 'w') as outf:
                outf.write('Titre, Categorie, URL, UPC, Prix Hors Taxe, Prix Avec Taxe, Nombre Disponible, Ratio des Vues\n')
                outf.write(str(informations[0]) + ' , '.rstrip('\n') + str(informations[1]) + ' , '.rstrip('\n') + str(informations[2]) + ' , '.rstrip('\n') + str(informations[3]) + ' , '.rstrip('\n') + str(informations[4]) + ' , '.rstrip('\n') + str(informations[5]) + ' , '.rstrip('\n') + str(informations[6]) + ' , '.rstrip('\n') + str(informations[7]))
    else:
        print("Erreur de requête. Veuillez retenter plus tard.")
        return(informations)

#fonction principale : scrap du ou des livres du site
def scrap_livre ():
    choix = int(input("Voulez-vous scrap un livre (tapez 1) ou le site entier (tapez 2) ? "))
    if choix == 1:
        livre = input("entrer l'url du livre que vous voulez 'scraper' : ")
        with open('urls_all_books.txt', 'r') as inf:
            for i in inf:
                if i.rstrip('\n') == livre: #IMPORTANT
                    stockage_Info(livre, choix)
                elif i == "" :
                    print("Aucun URL ne correspond.")
    elif choix == 2:
        with open('urls_all_books.txt', 'r') as inf:
            for url in inf:
                stockage_Info(url.rstrip('\n'), choix)
    else:
        print("Un problème est survenu. Peut-etre avez-vous mal exprimer votre demande, veuillez relancer le programme.")
    return

scrap_livre()

    #1) scrap livre : fait.
    #2) scrap category. (a modifier si le programme actuel ne convient pas).
    #3) scrap all website : Fait (quasiment).
