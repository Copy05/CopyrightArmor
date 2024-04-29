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
import hashlib
import json
import re

from bs4 import BeautifulSoup
from colorama import Style, Fore
from urllib.parse import urljoin
from IO import extract_domain, LoadIgnoreFileExts

def ScanTitle(title, my_content):
    with open('patterns.json', 'r') as file:
        patterns = json.load(file)['patterns']

    anime_pattern = re.compile(patterns['anime_pattern'], re.IGNORECASE)
    turkish_pattern = re.compile(patterns['turkish_pattern'], re.IGNORECASE) # Some may include Turkish Language.
    pirated_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns['pirated_patterns']]
    resolution_pattern = re.compile(patterns['resolution_pattern'], re.IGNORECASE)
    episode_pattern = re.compile(patterns['episode_pattern'], re.IGNORECASE)
    staffel_pattern = re.compile(patterns['staffel_pattern'], re.IGNORECASE)
    legal_sites_pattern = re.compile(patterns['legal_sites_pattern'], re.IGNORECASE)
    anime_deep_pattern = re.compile(patterns['anime_deep_pattern'], re.IGNORECASE)
    manga_chapter_pattern = re.compile(patterns['manga_chapter_pattern'], re.IGNORECASE)
    manga_online_pattern = re.compile(patterns['manga_online_pattern'], re.IGNORECASE)

    if my_content not in title:
        return False

    # Check for the presence of "Watch Anime" in the title
    if "Watch Anime" in title:
        return True
    
    if anime_pattern.match(title) or turkish_pattern.match(title):
        return True
    for pattern in pirated_patterns:
        if re.match(pattern, title):
            return True
    if episode_pattern.match(title) or staffel_pattern.match(title):
        return True
    if manga_chapter_pattern.match(title) or manga_online_pattern.match(title):
        return True
    if legal_sites_pattern.search(title):
        return False
    if anime_deep_pattern.match(title):
        return True
    if resolution_pattern.match(title):
        return True
    return False

def ScanGoogleLink(url, title, DebugInformation=False, verbose=False):
    from GoogleScrape import SearchQuery, infriding_data, UniqueFiles, infringing_urls

    titles_list = []
    contentFlagged = False

    Query = SearchQuery.replace("+", " ").replace('%2C', ',').replace('%20', ' ')

    if verbose:
        print(f"{Fore.YELLOW}URL: {url}\nTitle: {title}{Style.RESET_ALL}")

    with open("hashes.json") as file:
        data = json.load(file)

    entertainment_data = data.get("entertainment", [])

    # For every entry inside the Entertainment data. the Show Name will be appended inside the list.
    for entry in entertainment_data:
        m_title = entry.get("title", "")
        titles_list.append(m_title)

    for content in titles_list:

        # to differentiate content we want to check if the title of the show is inside the search result title like: "Watch SHOW1" -- "SHOW1"
        # like: "Watch SHOW1" -- "SHOW1" so that it get's flagged as "SHOW1"
        if ScanTitle(title, content) and content.lower() in title.lower():
            if verbose:
                print(f"{Fore.RED}COPYRIGHTED MATERIAL FOUND{Style.RESET_ALL}")
            contentFlagged = True
        else:
            if verbose:
                print(f"{Fore.GREEN}LEGAL{Style.RESET_ALL}")
            contentFlagged = False
        
        # to differentiate content we want to check if the title of the show is inside the search result title 
        # like: "Watch SHOW1" -- "SHOW1" so that it get's flagged as "SHOW1"
        if contentFlagged and content.lower() in title.lower():
            for entry in data['entertainment']:

                if entry['title'].lower() in content.lower():

                    original_owner = entry["copyright_owner"]
                    original_source = entry["original_url"]

                    # If the URL is the original source
                    if url == original_source:
                        continue
                            
                    infringing_urls.add(url)
                    UniqueFiles.add(url)

                    infriding_data.append({
                        "url": url,
                        "type": "Copyrighted Show",
                        "original_url": original_source,
                        "copyright_owner": original_owner,
                        "description": entry['title'],
                    })

                    if verbose:
                        print(Fore.RED, f"\nCopyright Infringing Show has been found on {url}.\nSearch Result Title: {title}\nCopyrighted Work: {entry['title']}\nCopyright Owner: {original_owner}\nOriginal Source: {original_source}\n")
                    else:
                        print(Fore.RED, f"\nCopyright Infringing Show has been found on {url}.\nCopyrighted Work: {entry['title']}\nCopyright Owner: {original_owner}\nOriginal Source: {original_source}\n")   
                    print(Style.RESET_ALL)

                    break

def ScanImage(soup : BeautifulSoup, url, DebugInformation : bool):
    from Scrape import ScannedImages, infriding_data, infringing_urls, TheBaseURL, UniqueFiles

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

                            if img_hash in UniqueFiles:
                                continue

                            infringing_urls.add(url)
                            UniqueFiles.add(img_hash)

                            infriding_data.append({
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

def ScanFiles(soup: BeautifulSoup, url, DebugInformation: bool):
    from Scrape import infriding_data, infringing_urls, TheBaseURL, Socials, UniqueFiles

    exts = LoadIgnoreFileExts()

    if soup:
        # Find all <a> tags
        links = soup.find_all('a')
        for link in links:
            link_text = link.get_text()
            link_url = link.get('href')

            if DebugInformation:
                if link_url and link_url != '/' and link_url != "/#":
                    print(Fore.MAGENTA, f"Found Link: {link_text} with href: {link_url}")

            if not link_url or link_url == '/' or link_url == "/#":
                continue

            if link_url and not any(link_url.endswith(ext) for ext in exts) and not any(link_url.startswith(social_link) for social_link in Socials):
                try:
                    link_content = requests.get(link_url).content
                except requests.exceptions.MissingSchema:
                    link_content = requests.get(urljoin(TheBaseURL, link_url)).content
                except (requests.exceptions.SSLError, requests.exceptions.InvalidSchema):
                    if DebugInformation:
                        print(Fore.RED, f"URL: {url} couln't be scanned. Skipping")
                    continue

                link_hash = hashlib.sha256(link_content).hexdigest()

                if DebugInformation:
                    print(Fore.MAGENTA, f"Found File Hash: {link_hash}")

                with open("hashes.json") as file:
                    data = json.load(file)

                for entry in data["files"]:
                    if entry["hash"] == link_hash:
                        original_owner = entry["copyright_owner"]
                        original_source = entry["original_url"]

                        base_domain_url = extract_domain(url)
                        base_domain_original = extract_domain(original_source)

                        if base_domain_url == base_domain_original:
                            continue

                        if link_hash in UniqueFiles:
                            continue

                        infringing_urls.add(url)
                        UniqueFiles.add(link_hash)

                        infriding_data.append({
                            "url": url,
                            "type": "Copyrighted File",
                            "original_url": original_source,
                            "copyright_owner": original_owner,
                            "description": entry['description'],
                            "hash": link_hash
                        })

                        print(Fore.RED, f"\nCopyright Infringing File (\"{link_hash}\") has been found on {url}.\nCopyright Owner: {original_owner}\nOriginal Source: {original_source}\n")
                        print(Style.RESET_ALL)

                        break