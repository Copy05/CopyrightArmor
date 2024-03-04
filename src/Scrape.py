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
import hashlib
import json

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import SSLError
from colorama import Style, Fore

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from IO import SaveReport, LoadSocialFilter, extract_domain
from checks import Checks
from verbose_print import PrintFoundLinks
from utils import GetSettings

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

TheQueue = queue.Queue()
visited_urls = set()
Found_Links = set()
infringing_urls = set()
image_data = []
Index = 1
InsideTheLoop = False
Socials = []
ignore_ssl = False

def ScrapeWebsite(url, depth=None, verbose=False, ReportFile=False, ReportFormat=".txt", RateLimmit=False, IgnoreSSL=False,
                  RateLimmitTime=2, ExternalVisits=False, DeepSearch=False, ExcludePaths=None, IncludeSocials=False, DebugInformation=False, GoogleScrape=False):
    
    global Index
    global InsideTheLoop
    global TheBaseURL
    global Socials
    global ignore_ssl
    global image_data

    SettingsString = GetSettings(RateLimmit, IgnoreSSL, ExternalVisits, DeepSearch, IncludeSocials)
    ScannedImages = set()

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

        if soup: 
            imgs = soup.find_all('img')
            for images in imgs:
                ScannedImages.add(images)
                image_url = images.get('src')

                if DebugInformation:
                    print(Fore.MAGENTA, f"Found Image Tags: {images} with source: {image_url}")

                if image_url:
                    try:
                        img_content = requests.get(image_url).content
                    except requests.exceptions.MissingSchema:
                        img_content = requests.get(urljoin(TheBaseURL, image_url)).content

                    img_hash = hashlib.sha256(img_content).hexdigest()

                    if DebugInformation:
                        print(Fore.MAGENTA, f"Found Image Hash: {img_hash}")

                    with open("hashes.json") as file:
                        data = json.load(file)

                    for entry in data["images"]:
                        if entry["hash"] == img_hash:
                            original_owner = entry["copyright_owner"]
                            original_source = entry["original_url"]
                            

                            base_domain_url = extract_domain(url)
                            base_domain_original = extract_domain(original_source)
                            
                            if base_domain_url == base_domain_original:
                                continue  

                            infringing_urls.add(url)

                            image_data.append({
                                "url": url,
                                "type": "Copyrighted Image",
                                "original_url": original_source,
                                "copyright_owner": original_owner,
                                "description": entry['description'],
                                "hash": img_hash
                            })
                            
                            print(Fore.RED, f"\nCopyright Infringing Image (\"{img_hash}\") has been found on {url}.\nCopyright Owner: {original_owner}\nOriginal Source: {original_source}\n")
                            print(Style.RESET_ALL)

                            break


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
                    SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, image_data=image_data, scanned_images=ScannedImages)
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
                    SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, image_data=image_data, scanned_images=ScannedImages)
                    exit()
    
    except SSLError:
        print(Fore.RED, f"URL: {url} has not a valid SSL Certificate. Skipping.")
        print(Style.RESET_ALL)
        pass

    except requests.exceptions.ConnectionError:
        print(Fore.RED, f"There is a issue with connecting to the site: {url}")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, image_data=image_data, scanned_images=ScannedImages)
            exit()

    except requests.exceptions.TooManyRedirects:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, image_data=image_data, scanned_images=ScannedImages)
            exit()

    except KeyboardInterrupt:
        print("Exiting Scrape Mode.")

        if ReportFile:
            SaveReport(URL=TheBaseURL, content=visited_urls, infriding_urls=infringing_urls, settings_string=SettingsString, image_data=image_data, scanned_images=ScannedImages)
            exit()
