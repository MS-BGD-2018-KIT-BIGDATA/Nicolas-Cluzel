import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


url_idf = "https://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&q=Renault%20Zoe"
url_paca = "https://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?o=1&q=Renault%20Zoe"
url_aquitaine = "https://www.leboncoin.fr/voitures/offres/aquitaine/?o=1&q=Renault%20Zoe"

def getSoupFromURL(url):
    # Gets the soup from the input url:
    
    res = requests.get(url)
    if res.status_code == 200:
        return BeautifulSoup(res.text, 'html.parser')

def getCarsDetailedURL():
    # Récupère la page détaillée de l'annonce:
             
    detailed_car_links = []   
    urls = [url_idf, url_paca, url_aquitaine]    
    url = "https://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&q=Renault%20Zoe"
    for url in urls:
        soup = getSoupFromURL(url)
        if soup:
            cars_info = soup.find_all("a", class_="list_item clearfix trackable")
            for el in cars_info:
                detailed_car_links.append("http:" + el['href']) 
    return detailed_car_links

def getDescription(detailed_url):
    # Récupère la description de l'annonce:
    
    soup = getSoupFromURL(detailed_url)
    if soup:
        desc = soup.find_all("p", class_="value")[0].text.strip()
    return desc

def getPhoneNumber(description):
    # Tente de récupérer un numéro de téléphone dans le contenu de l'annonce:
    
    test = re.findall("\d{2}[-\.\s]\d{2}[-\.\s]\d{2}[-\.\s]\d{2}[-\.\s]\d{2}",
                      description)  
    return test

def getArgus(annee):
    # Récupère l'argus du modèle en fonction de son année sur le site de la centrale:
    
    url = "https://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-" + str(annee) + ".html"
    soup = getSoupFromURL(url)
    if soup:
        argus = soup.find_all("span", class_="jsRefinedQuot")[0].text
    return argus
    

def getCarsFeatures(detailed_url):
    # Récupère les attributs des voitures scrapées:
        
    features = {}
    soup = getSoupFromURL(detailed_url)
    car_features = []
    car_vals = []
    pro_status = []
    argus = 0
    if soup :
        car_properties = soup.find_all("span", class_="property")
        car_values = soup.find_all("span", class_="value")
        pro_status = soup.find("span", class_="ispro")
        for el in car_properties:
            car_features.append(el.text.strip())        
        for el in car_values:
            car_vals.append(el.text.strip().replace(u'\xa0', u' '))
        car_features.append('Phone Number')
        car_features.append('Pro_Part')   
        car_vals.append(getPhoneNumber(getDescription(detailed_url)))       
        if pro_status:           
            car_vals.append('Professionnel')
        else:
            car_vals.append('Particulier')
        for i in range(0, len(car_features)):
            features[car_features[i]] = car_vals[i]
        argus = getArgus(features['Année-modèle'])
        features['Argus'] = argus

        
    return features
  
def getDataFrame(liste):
    # Crée un dataframe à partir des différentes infos récupérées:
    
    df_zoe = pd.DataFrame(liste)
    df_zoe = df_zoe.drop(['Référence', 'Carburant',
                          'Boîte de vitesse', 'Marque', 'Ville'], axis = 1)
    df_zoe['Prix'] = df_zoe['Prix'].str.split('€').str[0]
    df_zoe['Prix'] = df_zoe['Prix'].str.split('\'').str[0]
    df_zoe['Kilométrage'] = df_zoe['Kilométrage'].str.split('KM').str[0]
    df_zoe['Prix'] = df_zoe['Prix'].str.split(' ').str[0] + df_zoe['Prix'].str.split(' ').str[1]
    df_zoe['Argus'] = df_zoe['Argus'].str.split(' ').str[0] + df_zoe['Argus'].str.split(' ').str[1]
    df_zoe['Kilométrage'] = df_zoe['Kilométrage'].str.split(' ').str[0] + df_zoe['Kilométrage'].str.split(' ').str[1]
    df_zoe[['Prix','Kilométrage', 'Argus']] = df_zoe[['Prix','Kilométrage', 'Argus']].apply(pd.to_numeric, errors='raise')
    df_zoe['Ratio Prix / Argus'] = df_zoe['Prix'] / df_zoe['Argus']

    
    return df_zoe

def getCarsList():
    # Récupère la liste des infos pour chaque voiture:
    
    cars_list = []
    for link in getCarsDetailedURL():
        cars_list.append(getCarsFeatures(link))     
    return cars_list

# Main execution
 
getDataFrame(getCarsList()).to_csv("Car_list.csv", sep=",")
print(getDataFrame(getCarsList())) 
