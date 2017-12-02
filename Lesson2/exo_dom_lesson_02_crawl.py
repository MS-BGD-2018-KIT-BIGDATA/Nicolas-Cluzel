import requests
from bs4 import BeautifulSoup


def url(int):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+str(int)
    return url


def getSoupFromURL(url, method='get', data={}):
    #Get the soup from the url.
    
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None


def getEurosPerInhabitant(url, classname, subtotal): 
    #Get the total of euros per inhabitant depending on the url and the subtotal A, B, C or D.
    
    soup = getSoupFromURL(url)
    if soup:
        if subtotal == 'A' or subtotal== 'a':
            euros_inhab = soup.find_all(class_=classname)[1].text
            return euros_inhab
        elif subtotal == 'B' or subtotal == 'b':
            euros_inhab = soup.find_all(class_=classname)[20].text
            return euros_inhab
        elif subtotal == 'C' or subtotal == 'c':
            euros_inhab = soup.find_all(class_=classname)[53].text
            return euros_inhab
        elif subtotal == 'D' or subtotal == 'd':
            euros_inhab = soup.find_all(class_=classname)[77].text
            return euros_inhab
        else:
            return 'Error, unexpected subtotal asked.'
    else:
        0


def getMeanPerStrate(url, classname, subtotal):
    #Get the mean per strate depending on the url and the subtotal A, B, C or D.

    soup = getSoupFromURL(url)
    if soup:
        if subtotal == 'A' or subtotal== 'a':
            euros_inhab = soup.find_all(class_=classname)[2].text
            return euros_inhab
        elif subtotal == 'B' or subtotal == 'b':
            euros_inhab = soup.find_all(class_=classname)[21].text
            return euros_inhab
        elif subtotal == 'C' or subtotal == 'c':
            euros_inhab = soup.find_all(class_=classname)[54].text
            return euros_inhab
        elif subtotal == 'D' or subtotal == 'd':
            euros_inhab = soup.find_all(class_=classname)[78].text
            return euros_inhab
        else:
            return 'Error, unexpected subtotal asked.'
    else:
        0


for i in range(2010, 2016):
    print('-----')
    print('Année ' + str(i))
    print('-----')
    print('Total des produits de fonctionnement de l\'année ' + str(i) +':')
    print(getEurosPerInhabitant(url(i), "montantpetit", 'A') + 'euros par habitant.')
    print('Moyenne de la strate: '+ getMeanPerStrate(url(i), "montantpetit", 'A')+ 'euros.')
    print('Total des charges de fonctionnement de l\'année ' + str(i) +':')
    print(getEurosPerInhabitant(url(i), "montantpetit", 'B') + 'euros par habitant.')
    print('Moyenne de la strate: '+ getMeanPerStrate(url(i), "montantpetit", 'B')+ 'euros.')
    print('Total des ressources d\'investissement de l\'année ' + str(i) +':')
    print(getEurosPerInhabitant(url(i), "montantpetit", 'C') + 'euros par habitant.')
    print('Moyenne de la strate: '+ getMeanPerStrate(url(i), "montantpetit", 'C')+ 'euros.')
    print('Total des emplois d\'investissement de l\'année ' + str(i) +':')
    print(getEurosPerInhabitant(url(i), "montantpetit", 'D') + 'euros par habitant.')
    print('Moyenne de la strate: '+ getMeanPerStrate(url(i), "montantpetit", 'D') + 'euros.')

    
    

