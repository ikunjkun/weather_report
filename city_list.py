import requests
import json
from bs4 import BeautifulSoup

if __name__ == "__main__":
    url = "https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv"
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    page_text = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(page_text.text,'lxml')
    tr_list = soup.select('#repo-content-pjax-container > div > div > div.Box.mt-3.position-relative > div.Box-body.p-0.blob-wrapper.data.type-csv.gist-border-0 > div.markdown-body > table > tbody >tr')
    city_list = {}
    for tr in tr_list:
        td_list = tr.find_all('td')
        city_list[td_list[3].string] = td_list[1].string
    with open('city_list.json','w') as f:
        json.dump(city_list,f)
        print("ok")
        
