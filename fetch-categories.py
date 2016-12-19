import urllib2,sys,codecs
from bs4 import BeautifulSoup

BASE_URL ="https://www.mercari.com/jp/category/3"

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

buffer = len("https://www.mercari.com/jp/category/")

def fetch_html(url):
	return urllib2.urlopen(url)

html = fetch_html(BASE_URL)
soup = BeautifulSoup(html, "html.parser")
alist = soup.select(".parts-nav a")
map = {}
for a in alist:
	category = a.get_text().strip()
	link = a.get("href")
	deep_html = fetch_html(link)
	
	soup = BeautifulSoup(deep_html, "html.parser")
	deep_alist = soup.select(".parts-nav a")	
	
	for deep_a in deep_alist:
		sub_category = deep_a.get_text().strip()
		sub_link = deep_a.get("href")

		grand_child_id = sub_link[buffer:].replace("/", "").strip()
		
		print category + "," + sub_category + "," + grand_child_id

