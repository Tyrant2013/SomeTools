#!/usr/bin/python
import requests
import bs4
response = requests.get('http://m.data.house.163.com/gz/product/0ReD.html')
soup = bs4.BeautifulSoup(response.text, 'html.parser')
divs = soup.select('div.dd_inner')
for div in divs:
    print div.contents[1].text,div.contents[3].text,div.contents[5].text
