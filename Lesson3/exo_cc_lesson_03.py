# Distance ville Ã  ville des 100 plus grandes villes de France
# Implanter des bureaux dans des communes; savoir quelle distance vont parcourir
# les commerciaux
# Le résultat est la matrice des distances, ecrite dans un fichier csv

# Etape 1: Recuperer la liste des 100 plus grandes villes
# Etape 2: Recuperer la matrice

import requests
import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup


api_key = "AIzaSyB4Bkjb5s2jE2rp2-VhH2TwthnjzGv7RLs"

def getSoupFromURL(url):
    # Gets the soup from the input url:
    
    res = requests.get(url)
    if res.status_code == 200:
        return BeautifulSoup(res.text, 'html.parser')


def getTop100():
    # Gets the list of the top100 most crowded french cities:
        
    liste100 = []    
    for i in range(0, 3):
        url = "http://www.toutes-les-villes.com/villes-population" + str(i+1) + ".html"
        soup = getSoupFromURL(url)
        if soup:
            cities = soup.find_all(class_="HomeTxtVert")
            for el in cities:
                if ".html" and "a class=\"HomeTxtVert\"" and "(" in str(el):
                    liste100.append(el.text.split(' (')[0])
    return liste100[:10]

def getDistanceMatrix(cities):
    # Gets the distance matrix of the cities given in input:
        
    cities = '|'.join(cities)
    input_matrix = requests.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + cities + "&destinations=" + cities + "&key=AIzaSyB4Bkjb5s2jE2rp2-VhH2TwthnjzGv7RLs")
    interm_matrix = json.loads(input_matrix.text)
    origin_cities = interm_matrix["origin_addresses"]
    destination_cities = interm_matrix["destination_addresses"]
    distances = []
    for i in range(0, len(origin_cities)):
        for j in range(0, len(destination_cities)):
            distances.append(interm_matrix["rows"][i]["elements"][j]["distance"]["value"] / 100)
    return np.asarray(distances).reshape(len(getTop100()), len(getTop100()))

distances_df = pd.DataFrame(getDistanceMatrix(getTop100()))
distances_df.columns = getTop100()
distances_df["Cities"] = getTop100()
distances_df.set_index("Cities", inplace = True)
distances_df.to_csv("Distances_matrix.csv", sep=",")

print(distances_df)






#print(json.loads(matrix_3.text))
#print(soup)
#https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=YOUR_API_KEY

#result = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Paris&destinations=Lyon&key=AIzaSyCq-8vkkYXpQ0nz3pDX-oU4thora76sx7o")

#result_2 = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=Paris|Lyon&destinations=Marseille|Nice&mode=bicycling&language=fr-FR")

#df = pd.DataFrame(matrix)

#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
#                                     mode="transit")                                  
#cities = '|'.join(getTop100())
#df = pd.DataFrame(getDistanceMatrix(getTop100()))
#matrix = client_maps.distance_matrix('Paris', 'Lyon')
#matrix_2 = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=Paris|Lyon&destinations=Marseille|Nice)
#matrix_3 = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + cities + "&destinations=" + cities + "&key=AIzaSyB4Bkjb5s2jE2rp2-VhH2TwthnjzGv7RLs")
#if result_2.status_code == 200:
#print(BeautifulSoup(result_2.text, 'html.parser'))
#print(getTop100())
#print(cities)