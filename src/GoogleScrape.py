import requests
import time
import warnings

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib3.exceptions import InsecureRequestWarning
from colorama import Style, Fore

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from IO import SaveReport
from verbose_print import PrintFoundLinks

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

Found_Links = set()
Index = 1
CookieBannerClicked = False

MORE_RESULTS_BUTTON_XPATHS = ["//*[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div", "//*[@id='kp-wp-tab-cont-overview']/div/div[2]/div/div/div[4]/a[1]/h3/div"]

def GoogleScrape(Query, verbose=False, ReportFile=False, RateLimmit=False, RateLimmitTime=2):
    
    global CookieBannerClicked

    URL = f"https://google.com/search?q={Query}&cs=0&filter=0"

    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    soup = None

    if RateLimmit:
        time.sleep(RateLimmitTime)

    try:
        res = requests.get(URL, verify=False)

        if res.status_code == 200:
            driver.get(URL)
            wait = WebDriverWait(driver, 2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

        if soup and verbose:
            for anchor_tag in soup.find_all('a', href=True):
                PrintFoundLinks(URL, anchor_tag)
        
        if soup:
            FoundLinkCount = 0
            for link in soup.find_all('a', href=True):
                next_url = urljoin(URL, link['href'])

                if next_url.startswith("mailto:"):
                    if verbose:
                        print(Fore.YELLOW, f"Skipping {next_url} because 'mailto' links arent allowed")
                        print(Style.RESET_ALL)
                    continue
                if next_url.startswith("javascript:"):
                    if verbose:
                        print(Fore.YELLOW, f"Skipping {next_url} because 'javascript' links arent allowed")
                        print(Style.RESET_ALL)
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

                for link in soup.find_all('a', href=True):
                    if verbose:
                        PrintFoundLinks(URL, link)
                    next_url = urljoin(URL, link['href'])
                    if next_url not in Found_Links and "google.com" not in next_url:
                        Found_Links.add(next_url)
                        FoundLinkCount += 1

                if CookieBannerClicked is False:
                    try:
                        cookie_banner = driver.find_element(By.XPATH, "//*[@id='CXQnmb']")
                        decline_button = cookie_banner.find_element(By.XPATH, "//*[@id='W0wltc']/div")
                        decline_button.click()
                        CookieBannerClicked = True
                    except Exception as e:
                        print(Fore.RED, f"Cookie Banner Not Found")
                        print(Style.RESET_ALL)
                        pass

                try:
                    print(Fore.GREEN, f"Searching [Links Found: {len(Found_Links)}]")
                    print(Style.RESET_ALL)

                    if verbose:
                        print(Fore.YELLOW, f"{FoundLinkCount} Links has been added to the List. | {len(Found_Links)} Links in the List")
                        print(Style.RESET_ALL)

                    for xpath in MORE_RESULTS_BUTTON_XPATHS:
                        try:
                            more_results_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                            more_results_button.click()
                            break
                        except Exception:
                            pass    

                except Exception as e:
                    for _ in range(10):  
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

                    print(Fore.RED, f"More Results Button Not Found")
                    print(Style.RESET_ALL)
                    pass
        
    except requests.exceptions.TooManyRedirects:
        print(Fore.RED, "Overloaded.")
        print(Style.RESET_ALL)

        if ReportFile:
            SaveReport(URL=f"Google_Search_{Query}", content=Found_Links, detailed=False, found_links=Found_Links)
            exit()

    except KeyboardInterrupt:
        print("Exiting Scrape Mode.")

        if ReportFile:
            SaveReport(URL=f"Google_Search_{Query}", content=Found_Links, detailed=False, found_links=Found_Links)
            exit()