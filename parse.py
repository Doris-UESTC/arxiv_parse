import urllib.request
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

s=requests.Session()
s.mount('https://', MyAdapter())
def get_pdf_arxiv(web_site,path):
    rep = urllib.request.urlopen(urllib.request.Request(web_site))
    page = rep.read().decode('utf-8')
    citation_title = re.findall('<meta name="citation_title" content="(.*?)"/>',page,re.S)
    print(citation_title)
    path+=(citation_title[0]+'.pdf')
    pdf_download = re.findall('<meta name="citation_pdf_url" content="(.*?)"/>',page,re.S)
    print(pdf_download[0])
    if (len(pdf_download) != 0):
        try:
            u = urllib.request.urlopen(pdf_download[0])
        except urllib.error.HTTPError:
            print(pdf_download[0], "url file not found")
            return
        block_sz = 8192
        with open(path, 'wb') as f:
            while True:
                buffer = u.read(block_sz)
                if buffer:
                    f.write(buffer)
                else:
                    break
        print("Sucessful to download " + path)

path=""
url_set=[]
for url in url_set:
    get_pdf_arxiv(url,path)