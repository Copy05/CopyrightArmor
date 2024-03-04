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

import datetime
import time
import os
import tempfile
import json

from urllib.parse import urlparse

def LoadSocialFilter() -> list[str]:
    with open('filters.json', 'r') as file:
        data = json.load(file)

    socials = data["socials"]
    return socials

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def SaveReport(URL: str, content: set, infriding_urls: set, settings_string : str, image_data : list[dict], scanned_images : set):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%y-%m-%d")
    milliseconds = int(time.time() * 1000)
    sanitized_url = URL.replace('https://', '').replace('/', '-').replace('.', '-').replace('+', '-').replace(':', '')
    filename = f"CA_report_{sanitized_url}_{formatted_date}_{milliseconds}.txt"

    if os.name == 'nt':
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, filename)

    domain_counts = {}
    with open(filename, 'w') as file:

        sorted_content = sorted(content)
        for url in sorted_content:
            domain = extract_domain(url)
            if domain in domain_counts:
                domain_counts[domain].add(url)
            else:
                domain_counts[domain] = {url}

        file.write("-----------------------------------------------------------------------\n")
        file.write("CopyrightArmor Scan Report\n")
        file.write("-----------------------------------------------------------------------\n\n")   
        file.write(f"Base (Start) URL: {URL}\n")
        file.write(f"Scan Date: {formatted_date.replace('-', '/')} {time.strftime('%H:%M:%S', time.gmtime())}\n")
        file.write(f"Scan Settings: {settings_string}\n")
        file.write("\n-----------------------------------------------\n")   
        file.write("Summary\n")
        file.write("-----------------------------------------------\n\n")   
        file.write(f"Total Websites Scanned: {len(content)}\n")
        file.write(f"Total Domains Scanned: {len(domain_counts)}\n")
        file.write(f"Total Images Scanned: {len(scanned_images)}\n")
        file.write(f"Total Infringing Content Found: {len(infriding_urls)}\n")
        file.write("\n-----------------------------------------------\n")   
        file.write("Scan Report:\n")
        file.write("-----------------------------------------------\n\n")   
        file.write("Scanned URLs:\n")

        # ------------------------------------------------------- #
        
        # Sort the URLs before writing them to the file
        sorted_content = sorted(content)
        for url in sorted_content:
            file.write(url + "\n")
            domain = extract_domain(url)
            if domain in domain_counts:
                domain_counts[domain].add(url)
            else:
                domain_counts[domain] = {url}

        
        # ------------------------------------------------------- #
        
        file.write("\n-----------------------------------------------\n")   
        file.write(f"Scanned Domains {len(domain_counts)}:\n")
        file.write("-----------------------------------------------\n\n") 

        # ------------------------------------------------------- #
        
        # Prints a list of how many of which domain has been scanned
        sorted_domains = sorted(domain_counts.items(), key=lambda x: len(x[1]), reverse=True)
        for domain, urls in sorted_domains:
            file.write(f"{domain} - {len(urls)} URLs\n")

        # --------------------------------------------------------------- #
                
        file.write("\n-----------------------------------------------\n")   
        file.write("Details:\n")
        file.write("-----------------------------------------------\n\n") 

        infriding_count = 1

        if infriding_urls:
            for data in image_data:
                file.write(f"{infriding_count}. URL: {data.get('url')}\n")
                file.write(f"Type: {data.get('type')}\n")
                file.write(f"Description: {data.get('description')}\n")
                file.write(f"Original Source: {data.get('original_url')}\n")
                file.write(f"Copyright Owner: {data.get('copyright_owner')}\n\n")
                infriding_count += 1
        else:
            file.write("No infriding content has been found.\n")

    print(f"File Saved under: {filename}")