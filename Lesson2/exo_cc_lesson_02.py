# Mesurer le taux de discount sur les ordinateurs Acer et Dell sur cdiscount

import requests
from bs4 import BeautifulSoup


def urlSearchBrand(brand):
    url_search = "https://www.cdiscount.com/search/10/ordinateur+portable"
    return url_search + brand + ".html#_his_"

def getSoupFromURL(url, method='get', data={}):
    # Gets the soup from the url passed in argument:
    
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

def getCompList(url):   
    # Gets a dictionnary of the first ten portable computers of the brand
    # specified in the url if at least ten are displayed on the page
    
  soup = getSoupFromURL(url)
  laptop_result = {}
  laptop_list = []
  selling_price_list = []
  selling_price_list_res = []
  old_price_list = []
  old_price_list_res = []
  
  if soup:
      nav = soup.select("ul li div form div div")
      
  for k in range (0, len(nav)):
      if "prdtPrSt" in str(nav[k]):
          old_price_list.append(nav[k].text)
          selling_price_list.append(nav[k+1].text)
          laptop_list.append(str(nav[k]
          .parent.parent.parent.parent.parent.parent
          .find(class_ = "prdtBTit")).split("<div class=\"prdtBTit\">")[-1]
          .split("</div>")[0]
          )

  selling_price_list = selling_price_list[2::3]
  old_price_list = old_price_list[2::3]    
  laptop_list = laptop_list[2::3]
  
  for el in old_price_list:
      old_price_list_res.append(int(el.split(",")[0])
      + ((int(el.split(",")[1])) / 100))
  
  for el in selling_price_list:
      selling_price_list_res.append(int(el.split("€")[0]) 
      + ((int(el.split("€")[1])) / 100))
  
  for i in range (0, 10):  
      laptop_result[laptop_list[i]] = (selling_price_list_res[i], old_price_list_res[i])   
  return laptop_result
       
def calcDiscount(a, b):
    # Give the percentage of price reduction:
        
    result = ((b - a) / b) * 100.0
    return result     

def decision(dict_a, dict_b):
    # Returns the most interesting computer:
        
    if dict_a[next(iter(dict_a))] > dict_b[next(iter(dict_b))]:
        return next(iter(dict_a))
    else:
        return next(iter(dict_b))


#----------------------- TESTING STAGE -------------------------

# Sets the urls to be tested, depending on the brand:
url_dell = urlSearchBrand("dell")
url_acer = urlSearchBrand("acer")

# Gets the first 10 (if existing) bargained computers for each brand:
dell_result = getCompList(url_dell)
acer_result = getCompList(url_acer)

# Only take the first one for each dictionary in order to compare them:
first_one_dell = next(iter(dell_result))
first_one_acer = next(iter(acer_result))
first_one_dell_prices = dell_result[first_one_dell]
first_one_acer_prices = acer_result[first_one_acer]
discount_dell_dict = {}
discount_acer_dict = {}

discount_dell_dict[first_one_dell] = calcDiscount(first_one_dell_prices[0], first_one_dell_prices[1])
discount_acer_dict[first_one_acer] = calcDiscount(first_one_acer_prices[0], first_one_acer_prices[1])
discount_dell = calcDiscount(first_one_dell_prices[0], first_one_dell_prices[1])
discount_acer = calcDiscount(first_one_acer_prices[0], first_one_acer_prices[1])

# Returns the decision over which one is the most interesting bargain:
decision_ = decision(discount_dell_dict, discount_acer_dict) 

# The first two prints are the first two computers of each brand dictionary.
# Then, the choice advice is given:
    
print(discount_dell_dict)
print(discount_acer_dict)
print('-------------------')
print('The most interesting bargain is: '+ decision_)


