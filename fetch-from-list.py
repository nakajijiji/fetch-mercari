import urllib2,sys,codecs
from bs4 import BeautifulSoup

BASE_URL ="https://www.mercari.com/jp/search/?"

def fetch_html(url):
	return urllib2.urlopen(url)

def build_url(category_grand_child, size_group, size_id):
	if size_group == None:
		return BASE_URL + "category_grand_child[" + category_grand_child + "]=1"
	else:
		return BASE_URL + "category_grand_child[" + category_grand_child + "]=1&size_group=" + size_group + "&size_id[" + size_id + "]=1"
	

def proceed(category_grand_child, size_group, size_id):
	url = build_url(category_grand_child, size_group, size_id)
	html = fetch_html(url)
	soup = BeautifulSoup(html, "html.parser")
	items = soup.select(".items-box")
	results = []
	for item in items:
		title =	item.select("h3")[0].get_text()
		image_url = item.select("img")[0].get("data-src")
		price = item.select(".items-box-price")[0].get_text()
		price = price[1:].replace(",", "").replace(" ", "")
		results.append((title, image_url, price))
	return results

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

category_file = sys.argv[1]
size_file = sys.argv[2]

groupid_to_sizeids = {}

with open(size_file) as f:
	for l in f.readlines():
		id, value, size_id = l.rstrip().split(",")
		if not id in groupid_to_sizeids:
			groupid_to_sizeids[id] = []
		groupid_to_sizeids[id].append((value, size_id))

with codecs.open(category_file, "r", "utf-8") as f:
	for l in f.readlines():
		category, sub_category, grand_child_id, size_group = l.rstrip().split(",")
		if size_group in groupid_to_sizeids:
			sizeids = groupid_to_sizeids[size_group]
			for sizeid in sizeids:
				results = proceed(grand_child_id, size_group, sizeid[1])
				for result in results:
					print category + "," + sub_category + "," + sizeid[0] + "," + result[0] + "," + result[1] + "," + result[2]
		else:
			results = proceed(grand_child_id, None, None)
			for result in results:
				print category + "," + sub_category + ",," + result[0] + "," + result[1] + "," + result[2]

