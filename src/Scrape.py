#
# (c) Copyright Copy05, 2023
#
# Scrape.py | The ScrapingEngine of CopyrightArmor.
#

import requests
import time
import queue
import warnings

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import SSLError
from colorama import Style, Fore

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from IO import SaveReport, LoadSocialFilter
from checks import Checks
from verbose_print import PrintFoundLinks

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

TheQueue = queue.Queue()
visited_urls = set()
Found_Links = set()
Index = 1
InsideTheLoop = False
Socials = []
ignore_ssl = False

def ScrapeWebsite(url, depth=None, verbose=False, MonitorMode=False, ReportFile=False, ReportFormat=".txt", RateLimmit=False, IgnoreSSL=False,
                  RateLimmitTime=2, IgnoreRobotTXT=False, EnableProxy=False, CustomUserAgent=None, ExternalVisits=False, DeepSearch=False, ExcludePaths=None, IncludeSocials=False, DebugInformation=False, GoogleScrape=False, DetailedReport=False):
    
    global Index
    global InsideTheLoop
    global TheBaseURL
    global Socials
    global ignore_ssl

    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    if InsideTheLoop is False:
        if IgnoreSSL is True:
            ignore_ssl = not IgnoreSSL
        if IncludeSocials is False:
            Socials = LoadSocialFilter()
        TheBaseURL = url

    if DebugInformation and not InsideTheLoop:
        print(Fore.MAGENTA, f"""BaseURL: {TheBaseURL}
URL: {url}
Rate Limmit Time: {RateLimmitTime}s

----- [ Command Line Arguments ] ------
RateLimmit: {RateLimmit}
IncludeSocials: {IncludeSocials}
DeepSearch: {DeepSearch}
DebugInformation: {DebugInformation}
Ignore SSL: {IgnoreSSL} (verify={ignore_ssl})
ExternalVisits: {ExternalVisits}""")
        print(Style.RESET_ALL)

    soup = None

    if url in visited_urls:
        return

    if depth is not None and depth <= 0:
        return
    
    if depth is not None:
        depth -= 1
     
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
    
    print(Fore.GREEN, f"({Index}) {url} [{Index}/{len(Found_Links)}] [{TheQueue.qsize()} left]")
    print(Style.RESET_ALL)

    if RateLimmit:
        time.sleep(RateLimmitTime)

    try:
        res = requests.get(url, verify=ignore_ssl)

        if res.status_code == 200:
            
            driver.get(url)
            wait = WebDriverWait(driver, 2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

        if soup and verbose:
            for anchor_tag in soup.find_all('a', href=True):
                foundurl = urljoin(url, anchor_tag['href'])
                PrintFoundLinks(url, anchor_tag)
                if GoogleScrape:
                    if "sca_esv=" not in foundurl:
                        Found_Links.add(foundurl)

        if soup:
            FoundLinkCount = 0
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])

                if next_url.startswith("javascript:") or next_url.startswith("mailto:") or next_url.startswith("tel:"):
                    if verbose:
                        print(Fore.YELLOW, f"Skipping {next_url} because these types of links arent allowed")
                        print(Style.RESET_ALL)
                    continue

                if IncludeSocials is False:
                    if any(next_url.startswith(social_link) for social_link in Socials):
                        if verbose:
                            print(Fore.YELLOW, f"Skipping {next_url}.")
                            print(Style.RESET_ALL)
                        continue

                if next_url.startswith(TheBaseURL) and not ExternalVisits:
                    if next_url not in visited_urls and next_url not in TheQueue.queue:
                        TheQueue.put(next_url)
                        Found_Links.add(next_url)
                        FoundLinkCount += 1
                if ExternalVisits is True:
                    if next_url not in visited_urls and next_url not in TheQueue.queue:
                        TheQueue.put(next_url)
                        Found_Links.add(next_url)
                        FoundLinkCount += 1

            if verbose:
                print(Fore.YELLOW, f"{FoundLinkCount} Links has been added to the Queue. | {TheQueue.qsize()} Links in the queue")
                print(Style.RESET_ALL)

            if InsideTheLoop is False:
                InsideTheLoop = True
                while not TheQueue.empty():
                    next_link = TheQueue.get()
                    ScrapeWebsite(next_link, depth=depth, RateLimmit=RateLimmit, verbose=verbose, ExternalVisits=ExternalVisits, DeepSearch=DeepSearch)
                if verbose:    
                    print(f"URL: {TheBaseURL}\nVisited URLs: {len(visited_urls)}\nFound Links: {len(Found_Links)}")
                driver.quit()
                if ReportFile:
                    SaveReport(URL=TheBaseURL, content=visited_urls, detailed=DetailedReport, found_links=Found_Links)
                    exit()

        else:
            if verbose:
                print(Fore.RED, f"The given URL \"{url}\" is invalid.", end=' ')
                print(Style.RESET_ALL)

            if InsideTheLoop is False:
                InsideTheLoop = True
                while not TheQueue.empty():
                    next_link = TheQueue.get()
                    ScrapeWebsite(next_link, depth=depth, RateLimmit=RateLimmit, verbose=verbose, ExternalVisits=ExternalVisits, DeepSearch=DeepSearch)
                if verbose:    
                    print(f"URL: {TheBaseURL}\nVisited URLs: {len(visited_urls)}\nFound Links: {len(Found_Links)}")
                driver.quit()
                if ReportFile:
                    SaveReport(URL=TheBaseURL, content=visited_urls, detailed=DetailedReport, found_links=Found_Links)
                    exit()
    
    except SSLError:
        print(Fore.RED, f"URL: {url} has not a valid SSL Certificate. Skipping.")
        print(Style.RESET_ALL)
        pass

    except requests.exceptions.ConnectionError:
        print(Fore.RED, f"There is a issue with connecting to the site: {url}")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, detailed=DetailedReport, found_links=Found_Links)
            exit()

    except requests.exceptions.TooManyRedirects:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, detailed=DetailedReport, found_links=Found_Links)
            exit()

    except KeyboardInterrupt:
        print("Exiting Scrape Mode.")

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, detailed=DetailedReport, found_links=Found_Links)
            exit()
