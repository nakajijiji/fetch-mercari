import urllib2,sys
from bs4 import BeautifulSoup

BASE_URL ="https://www.mercari.com/jp/search/?"

category_root = sys.argv[1]
category_child = sys.argv[2]
size_group = sys.argv[3]

url = BASE_URL + "category_root=" + category_root + "category_child=" + category_child + "size_group=" + size_group 

def fetch_html(url):
	return urllib2.urlopen(url)

html = fetch_html(url)
soup = BeautifulSoup(html, "html.parser")
items = soup.select(".items-box")

for item in items:
	title =	item.select("h3")[0].get_text()
	image_url = item.select("img")[0].get("data-src")
	price = item.select(".items-box-price")[0].get_text()
	price = price[1:].replace(",", "").replace(" ", "")
	print title + "," + image_url + "," + price
	
