#
# (c) Copyright Copy05, 2023
#
# Scrape.py | The ScrapingEngine of CopyrightArmor.
#

import requests
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Style, Fore

from IO import SaveReport
from checks import Checks
from verbose_print import PrintFoundLinks

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
        Checks.ExcludePaths(Verbose=verbose, ExcludePath=ExcludePaths, Visted_URLs=visited_urls)
    
    parsed_url = urlparse(url)
    # If the HTTP Link is Invalid then it returns True
    if Checks.InvalidHttp(url, parsed_url, verbose) is True:
        return
    
    # If DeepSearch is False, it returns False
    if Checks.QueryParameter(url, parsed_url, DeepSearch=DeepSearch, Verbose=verbose) is False:
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
                PrintFoundLinks(url, anchor_tag)

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
