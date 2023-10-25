import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Style, Fore
from IO import SaveReport

visited_urls = set()
Index = 1

def ScrapeWebsite(url, depth=1, verbose=False, MonitorMode=False, ReportFile=False, ReportFormat=".txt", RateLimmit=False,
                  RateLimmitTime=2, IgnoreRobotTXT=False, EnableProxy=False, CustomUserAgent=None, HeadlessBrowser=False, ExternalVisits=False, DeepSearch=False, ExcludePaths=None):
    
    global Index

    soup = None

    if url in visited_urls:
        return
     
    visited_urls.add(url)
    Index += 1

    if ExcludePaths is not None:
        print("Adding URLs from: ", ExcludePaths)
        with open(ExcludePaths, 'r') as file:
            for line in file:
                cleanline = line.strip()
                if verbose:
                    print("Add URL: ", cleanline)
                visited_urls.add(cleanline)
    
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'http' and parsed_url.scheme != 'https':
        if verbose:
            print(Fore.YELLOW, f"Skipped URL with invalid scheme: {url}")
            print(Style.RESET_ALL)
        return
    
    if not DeepSearch and parsed_url.query:
        if verbose:
            print(Fore.YELLOW, f"Skipped URL with query parameters: {url}")
            print(Style.RESET_ALL)
        return
    
    print(Fore.GREEN, f"({Index}) {url}", end=' ')
    print(Style.RESET_ALL)

    if RateLimmit:
        time.sleep(RateLimmitTime)

    try:
        res = requests.get(url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')

        if soup and verbose:
            for anchor_tag in soup.find_all('a', href=True):
                print(Fore.YELLOW, f"Anchor Tag: {urljoin(url, anchor_tag['href'])}")
                print(f"Anchor Text: {anchor_tag.text.strip()}")
                print(Style.RESET_ALL)

        if soup and not ExternalVisits:
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if next_url.startswith(url):
                    ScrapeWebsite(next_url, RateLimmit=RateLimmit, verbose=verbose, ExternalVisits=ExternalVisits, 
                  DeepSearch=DeepSearch)
        else:
            if verbose:
                print(Fore.RED, f"The given URL \"{url}\" is invalid.", end=' ')
                print(Style.RESET_ALL)
                
    except requests.exceptions.TooManyRedirects:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)
        if ReportFile:
            SaveReport(visited_urls)
            exit()

    except KeyboardInterrupt:
        print("Exiting Scrape Mode.")

        if ReportFile:
            SaveReport(visited_urls)
            exit()
