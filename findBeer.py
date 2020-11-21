from bs4 import BeautifulSoup
import requests

def extract_title(content, searchTag):
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find("title", text=True)

    if not tag or tag.string.lower().find(searchTag) < 0 :
        return None
    
    return tag.string.strip()

def extract_links(content, searchTag):
        soup = BeautifulSoup(content, "lxml")
        links = set()

        for tag in soup.find_all("a", href=True):
            if tag["href"].startswith("http") and tag["href"].lower().find(searchTag) > -1:
                links.add(tag["href"])

        return links

def beerCrawler(start_url, searchTag):
    seen_urls = set([start_url])
    available_urls = set([start_url])

    while available_urls:
        url = available_urls.pop()

        try:
            content = requests.get(url, timeout=3).text                
        except Exception:
            continue

        title = extract_title(content, searchTag)

        if title:
            print(title)
            print(url)
            print()

        for link in extract_links(content, searchTag):
            if link not in seen_urls:
                seen_urls.add(link)
                available_urls.add(link)

try:
    searchTag = input('Qual cerveja deseja procurar hoje? ')
    beerCrawler("https://www.angeloni.com.br/super/busca?Nrpp=48&Ntt="+searchTag.lower(), searchTag.lower())
except KeyboardInterrupt:
    print()
    print("Bye beer lover!")