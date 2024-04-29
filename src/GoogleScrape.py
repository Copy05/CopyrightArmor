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
import warnings

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
from colorama import Style, Fore

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from IO import SaveReport, LoadWhitelist, extract_domain
from verbose_print import PrintFoundLinks
from ContentMatching import ScanGoogleLink
from ScrapingEngine import FilterLinks
from utils import GetSettings

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--remote-debugging-pipe")

driver = webdriver.Chrome(options=chrome_options)

Found_Links = set()
ScannedImages = set()
UniqueFiles = set()
infringing_urls = set()
infriding_data = []
Index = 1
CookieBannerClicked = False
SearchQuery = None

MORE_RESULTS_BUTTON_XPATHS = ["//*[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div", "//*[@id='kp-wp-tab-cont-overview']/div/div[2]/div/div/div[4]/a[1]/h3/div", "//*[@id='kp-wp-tab-cont-overview']/div/div[2]/div/div/div[4]/a[2]/h3/span", "//*[@id='kp-wp-tab-cont-overview']/div/div[3]/div/div/div[4]/a[1]/h3/div", "//*[@id='botstuff']/div/div[4]/div[4]/a[1]/h3/div", "//*[@id='kp-wp-tab-cont-TvmWatch']/div/div[3]/div/div/div[4]/a[1]/h3/div"]

def GoogleScrape(Query, verbose=False, ReportFile=False, RateLimmit=False, RateLimmitTime=2):
    
    global CookieBannerClicked
    global SearchQuery

    URL = f"https://google.com/search?q={Query}&cs=0&filter=0&safe=off&nfpr=1"

    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    soup = None
    MAXIMAL_RETRIES = 3
    Retries = 0
    SearchQuery = Query
    whitelist = LoadWhitelist()
    

    if RateLimmit:
        time.sleep(RateLimmitTime)

    try:
        res = requests.get(URL)
        if res.status_code == 200:
            driver.get(URL)
            wait = WebDriverWait(driver, 2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

        if res.status_code == 429:
            if 'Retry-After' in res.headers:
                print(Fore.RED, f"429 Too Many Requests. | You've send too many requests to Google. Please try in {res.headers['Retry-After']} seconds again!")
            else:
                print(Fore.RED, f"429 Too Many Requests. | You've send too many requests to Google. Please try later again!")
                
            print(Style.RESET_ALL)
            exit(0)
        if soup and verbose:
            for anchor_tag in soup.find_all('a', href=True):
                PrintFoundLinks(URL, anchor_tag)
        
        if soup:
            FoundLinkCount = 0
            for link in soup.find_all('a', href=True):
                next_url = urljoin(URL, link['href'])

                if FilterLinks(next_url, verbose, True):
                    continue

                if next_url not in Found_Links and "google.com" not in next_url:
                    Found_Links.add(next_url)
                    FoundLinkCount += 1
                
            if verbose:
                print(Fore.YELLOW, f"{FoundLinkCount} Links has been added to the List. | {len(Found_Links)} Links in the List")
                print(Style.RESET_ALL)

            while True:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                FoundLinkCount = 0
                FoundAnyLinks = False

                for link in soup.find_all('a', href=True):
                    if verbose:
                        PrintFoundLinks(URL, link)
                    next_url = urljoin(URL, link['href'])
                    if next_url not in Found_Links and "google.com" not in next_url:
                        Found_Links.add(next_url)
                        FoundLinkCount += 1
                        FoundAnyLinks = True
                        
                        if extract_domain(next_url) not in whitelist:
                            ScanGoogleLink(url=next_url, title=link.text.strip(), verbose=verbose, DebugInformation=False)
                        
                if CookieBannerClicked is False:
                    try:
                        cookie_banner = driver.find_element(By.XPATH, "//*[@id='CXQnmb']")
                        decline_button = cookie_banner.find_element(By.XPATH, "//*[@id='W0wltc']/div")
                        decline_button.click()
                        CookieBannerClicked = True
                    except Exception:
                        print(Fore.RED, f"Cookie Banner Not Found")
                        print(Style.RESET_ALL)
                        pass

                try:
                    print(f"{Fore.GREEN}Searching [Links Found: {len(Found_Links)}] {Fore.WHITE}| {Fore.RED}Infriding Links Found: {len(infriding_data)}{Style.RESET_ALL}")

                    if verbose:
                        print(Fore.YELLOW, f"{FoundLinkCount} Links has been added to the List. | {len(Found_Links)} Links in the List")
                        print(Style.RESET_ALL)

                    for _ in range(10):  
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

                    if not FoundAnyLinks:
                        Retries += 1
                    else:
                        Retries = 0

                    if Retries > MAXIMAL_RETRIES:
                        break

                    # The "More Results Button" has multiple XPATHS
                    for xpath in MORE_RESULTS_BUTTON_XPATHS:
                        try:
                            more_results_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                            more_results_button.click()
                            break
                        except Exception:
                            pass    

                except Exception:
                    for _ in range(10):  
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                    pass

            print(f"Query: {Query}\nFound Links: {len(Found_Links)}\n{Fore.RED}Infriding Search Results: {len(infriding_data)}{Style.RESET_ALL}")
            if ReportFile:
                SaveReport(URL=f"Google_Search_{Query}", content=Found_Links, settings_string=GetSettings(RateLimmit, False, False, False, False), infriding_data=infriding_data, infriding_urls=infringing_urls, scanned_images=ScannedImages)
            exit()

    except requests.exceptions.TooManyRedirects:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=f"Google_Search_{Query}", content=Found_Links, settings_string=GetSettings(RateLimmit, False, False, False, False), infriding_data=infriding_data, infriding_urls=infringing_urls, scanned_images=ScannedImages)
        exit()

    except KeyboardInterrupt:
        print("Exiting Scrape Mode.")

        if ReportFile:
            SaveReport(URL=f"Google_Search_{Query}", content=Found_Links, settings_string=GetSettings(RateLimmit, False, False, False, False), infriding_data=infriding_data, infriding_urls=infringing_urls, scanned_images=ScannedImages)
        exit()