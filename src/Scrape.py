# Copyright (c) 2023 - 2024 Copy05
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import requests
import time
import queue
import warnings
import urllib3

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
from utils import GetSettings
from ContentMatching import ScanImage, ScanFiles
from ScrapingEngine import AddToQueue, FilterLinks

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--remote-debugging-pipe")

driver = webdriver.Chrome(options=chrome_options)

TheQueue = queue.Queue()

# Filters
Socials = []

# URL Sets
visited_urls = set()
Found_Links = set()
infringing_urls = set()

# Image Data
ScannedImages = set()
UniqueFiles = set()
infriding_data = []

# Flags
InsideTheLoop = False
ignore_ssl = False

# Counters
Index = 1
FoundLinkCount = 0

def ScrapeWebsite(url, depth=None, verbose=False, ReportFile=False, ReportFormat=".txt", RateLimmit=False, IgnoreSSL=False,
                  RateLimmitTime=2, ExternalVisits=False, DeepSearch=False, ExcludePaths=None, IncludeSocials=False, DebugInformation=False, GoogleScrape=False):
    
    global Index
    global InsideTheLoop
    global TheBaseURL
    global Socials
    global ignore_ssl
    global infriding_data
    global ScannedImages
    global FoundLinkCount

    SettingsString = GetSettings(RateLimmit, IgnoreSSL, ExternalVisits, DeepSearch, IncludeSocials)

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
            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            soup = BeautifulSoup(driver.page_source, 'html.parser')

        ScanImage(soup, url, DebugInformation)
        ScanFiles(soup, url, DebugInformation)

        if soup and verbose:
            for anchor_tag in soup.find_all('a', href=True):
                foundurl = urljoin(url, anchor_tag['href'])
                PrintFoundLinks(url, anchor_tag)
                if GoogleScrape:
                    if "sca_esv=" not in foundurl:
                        Found_Links.add(foundurl)

        if soup:
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])

                # Filtering Socials and javascript: / mailto: links out
                if FilterLinks(next_url, verbose, IncludeSocials):
                    continue

                # If external visits is false. dont leave the page
                if next_url.startswith(TheBaseURL) and not ExternalVisits:
                    AddToQueue(next_url)
                # If External visits is true. they can leave the page
                if ExternalVisits is True:
                    AddToQueue(next_url)

            if verbose:
                print(Fore.YELLOW, f"{FoundLinkCount} Links has been added to the Queue. | {TheQueue.qsize()} Links in the queue")
                print(Style.RESET_ALL)

            if InsideTheLoop is False:
                InsideTheLoop = True
                while not TheQueue.empty():
                    next_link = TheQueue.get()
                    ScrapeWebsite(next_link, depth=depth, RateLimmit=RateLimmit, verbose=verbose, ExternalVisits=ExternalVisits, DeepSearch=DeepSearch, DebugInformation=DebugInformation)
                if verbose:    
                    print(Fore.YELLOW, f"URL: {TheBaseURL}\nVisited URLs: {len(visited_urls)}\nFound Links: {len(Found_Links)}\n{Fore.RED}Infriding Content: {len(infringing_urls)}")
                    print(Style.RESET_ALL)
                driver.quit()
                if ReportFile:
                    SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
                exit()

        else:
            if verbose:
                print(Fore.RED, f"The given URL \"{url}\" is invalid.", end=' ')
                print(Style.RESET_ALL)

            if InsideTheLoop is False:
                InsideTheLoop = True
                while not TheQueue.empty():
                    next_link = TheQueue.get()
                    ScrapeWebsite(next_link, depth=depth, RateLimmit=RateLimmit, verbose=verbose, ExternalVisits=ExternalVisits, DeepSearch=DeepSearch, DebugInformation=DebugInformation)
                if verbose:    
                    print(Fore.YELLOW, f"URL: {TheBaseURL}\nVisited URLs: {len(visited_urls)}\nFound Links: {len(Found_Links)}\n{Fore.RED}Infriding Content: {len(infringing_urls)}")
                    print(Style.RESET_ALL)
                driver.quit()
                if ReportFile:
                    SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
                exit()
    
    except SSLError:
        print(Fore.RED, f"URL: {url} has not a valid SSL Certificate. Skipping.")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
        exit()

    except requests.exceptions.ConnectionError:
        print(Fore.RED, f"There is a issue with connecting to the site: {url}")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
        exit()

    except requests.exceptions.TooManyRedirects:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
        exit()

    except urllib3.exceptions.MaxRetryError:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)


        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
        exit()

    except KeyboardInterrupt:
        print("Exiting Scrape Mode.")

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, infriding_data=infriding_data, scanned_images=ScannedImages)
        exit()
