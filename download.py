import requests
from bs4 import BeautifulSoup
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("url", help="Enter the website page url to download" ,type=str)
args = parser.parse_args()
print(args.url)

# specify the URL of the archive here
archive_url = args.url

def get_media_links():
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content,'html5lib')
    links = soup.find_all('a', href=True)
    filteredLinks = list(filter(lambda x: x['href'].endswith('.html'),links))
    ultLink = []
    for link in filteredLinks:
        ultLink.append("https:"+link['href'].strip(".html"))

    return ultLink

def download_media_batch(links):
    for link in links:
        file_name = link.split('/')[-2:]
        file_name = '/'.join(file_name)
        print("Downloading file:%s"%file_name)          
        # create response object 
        r = requests.get(link, stream = True) 
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
                # download started 
        with open(file_name, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 
          
        print ("%s downloaded!\n"%file_name)
  
    print ("All downloaded!")

    return

if __name__ == '__main__':
    linksToDownload = get_media_links()
    for link in linksToDownload:
        print(link)
    download_media_batch(linksToDownload)
