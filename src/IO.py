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

def SaveReport(URL: str, content: set, detailed: bool, found_links: set):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%m-%d-%y")
    milliseconds = int(time.time() * 1000)
    sanitized_url = URL.replace('https://', '').replace('/', '-').replace('.', '-').replace('+', '-').replace(':', '')
    filename = f"CA_report_{sanitized_url}_{formatted_date}_{milliseconds}.txt"

    if os.name == 'nt':
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, filename)

    domain_counts = {}
    found_domains = {}
    with open(filename, 'w') as file:
        file.write(f"CopyrightArmor {formatted_date.replace('-', '/')} Report\nBase URL: {URL}\n\nScanned URLs ({len(content)}):\n")
        
        # Sort the URLs before writing them to the file
        sorted_content = sorted(content)
        for url in sorted_content:
            file.write(url + "\n")
            domain = extract_domain(url)
            if domain in domain_counts:
                domain_counts[domain].add(url)
            else:
                domain_counts[domain] = {url}

        # Prints a list of how many of which domain has been scanned
        file.write(f"\nScanned Domains ({len(domain_counts)}):\n")
        sorted_domains = sorted(domain_counts.items(), key=lambda x: len(x[1]), reverse=True)
        for domain, urls in sorted_domains:
            file.write(f"{domain} - {len(urls)} URLs\n")

        if detailed:
            file.write(f"\nFound Links ({len(found_links)}):\n")
            
            # Sort the found_links before writing them to the file
            sorted_found_links = sorted(found_links)
            for link in sorted_found_links:
                file.write(f"{link}\n")
                domain = extract_domain(link)
                if domain in found_domains:
                    found_domains[domain].add(link)
                else:
                    found_domains[domain] = {link}

            # Prints a list of how many of which domain has been FOUND
            file.write(f"\nFound Domains ({len(found_domains)}):\n")
            sorted_domains = sorted(found_domains.items(), key=lambda x: len(x[1]), reverse=True)
            for domain, urls in sorted_domains:
                file.write(f"{domain} - {len(urls)} URLs\n")

    print(f"File Saved under: {filename}")