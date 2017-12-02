import requests
import pandas as pd
import numpy as np
import json
import re
from bs4 import BeautifulSoup

# Aller récupérer des infos sur open medicaments des infos
# Notamment les contre-indications (age, kg)

def getSoupFromURL(url):
    # Gets the soup from the input url:
    
    res = requests.get(url)
    if res.status_code == 200:
        return BeautifulSoup(res.text, 'html.parser')


def getMedFeatures():
    # Récupère les attributs des medicaments scrapés:
    
    test = requests.get("https://open-medicaments.fr/api/v1/medicaments/63605055")    
    json_f = json.loads(test.text)
    name = json_f.get('denomination')
    price = json_f.get('price')
    date = json_f.get('dateAMM')
    composition = json_f.get('compositions')
    dosage = json_f.get('compositions')[0].get('substancesActives')[0].get('dosageSubstance')
    titulaires = json_f.get('titulaires')[0]
    prescription = json_f.get('conditionsPrescriptionDelivrance')
    presentations = json_f.get('presentations')[0].get('libelle')
    nb_comprimes = re.findall('\d+', presentations)[0]
    cntr_indications = json_f.get('indicationsTherapeutiques')
    poids = re.findall('\d{2}[-\.\s]', cntr_indications)[0].split()[0]
    age = re.findall('(\d+) ans', cntr_indications)[0].split()[0]
    features = {}
    #re_test = ''
    regex = re.compile('\d+')    
    re_test = re.findall('\d+', dosage)
    features = {}
    attributs = ['name', 'price', 'date', 'dosage', 'titulaires', 'nb_comprimes', 'poids_min', 'age_min']
    valeurs = [name, price, date, dosage, titulaires, nb_comprimes, poids, age]
    
    for i in range (0, len(attributs)):
        features[attributs[i]] = valeurs[i]
    
    return features

# Main execution:

print(getMedFeatures())




