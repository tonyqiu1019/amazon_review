import requests, random, uuid
from credential import proxies

headers = [
	{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'},
	{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'},
	{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'},
	{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/13.10586'},
	{'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64, x64; Trident/7.0; rv:11.0) like Gecko'},
]

def write_html(data, filename='sample.html'):
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(data.content.decode('utf-8'))

def select_headers():
	idx = random.randint(0, len(headers)-1)
	return headers[idx]

def select_proxies():
	idx = random.randint(0, len(proxies)-1)
	return proxies[idx]

def load_html(url):
	header = select_headers()
	proxy = select_proxies()
	filename = str(uuid.uuid1())
	page = requests.get(url, headers = header, proxies=proxy)

	write_html(page, "/af12/jw7jb/public_html/%s.html"%(filename))
	with open("/af12/jw7jb/public_html/proxy_log.txt", 'a', encoding='utf-8') as f:
		f.write("%s\n %s\n %s\n %s\n"%(filename, url, header['User-Agent'], proxy['https']))

	page_response = page.text
	return page_response
