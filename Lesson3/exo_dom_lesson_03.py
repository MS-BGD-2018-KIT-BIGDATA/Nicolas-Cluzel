import requests
import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup


url = "https://gist.github.com/paulmillr/2657075"

token = 'fba2e4d40c519642b4799d58048762e22f9dd20c'
headers = {'Authorization' : 'Token ' + token}

def getSoupFromURL(url):
    # Gets the soup from the input url:
    
    res = requests.get(url)
    if res.status_code == 200:
        return BeautifulSoup(res.text, 'html.parser')
    
    
def getTop256Names(url, tags):
    # Gets a dictionnary of the top 256 contributors, displaying their rank
    # as a key, and their pseudonym (Name) as a value:
    
    soup = getSoupFromURL(url)
    rankings = {}
    users = []
    name = ''
    if soup:
        for k in range(1, 257):            
                name = soup.select(tags)[(k-1) * 4].text
                users.append(soup.select(tags)[(k-1) * 4].text.split(" ")[0])
                rankings[k] = name
    return rankings, users

def getMeanOfStars(user):
    # Gets the mean of stars for the total repositories of a given user:
        
    url_repos = "https://api.github.com/users/" + user + "/repos"
    page = requests.get(url_repos, headers = headers)
    stars_list = []
    stars_total = 0
    
    repos = json.loads(page.content)
    for repo in repos:
        stars_list.append(repo['stargazers_count'])
    
    if (len(stars_list) !=0):
        for star in stars_list:
            stars_total += star
        return stars_total / len(stars_list)    
    else :
        return 0
    
# Main execution
    
print(getTop256Names(url, "table tbody tr td")[0])

user_stars = []
for user in getTop256Names(url, "table tbody tr td")[1]:
    user_stars.append(getMeanOfStars(user))

df_rankings = pd.DataFrame()
df_rankings['Users'] = np.asarray(getTop256Names(url, "table tbody tr td")[1])
df_rankings['Stars'] = np.asarray(user_stars)
df_rankings = df_rankings.sort_values(by=['Stars'], ascending=False)

print(df_rankings)