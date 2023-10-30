#
# (c) Copyright Copy05, 2023
#
# IO.py | Input & Output files
#

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

def SaveReport(content: set):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%m-%d-%y")
    milliseconds = int(time.time() * 1000)
    filename = f"CA_report_{formatted_date}_{milliseconds}.txt"

    if os.name == 'nt':
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, filename)

    domain_counts = {}
    with open(filename, 'w') as file:
        file.write(f"CopyrightArmor {formatted_date.replace('-', '/')} Report\n\nScanned URLs ({len(content)}):\n\n")
        for url in content:
            file.write(url + "\n")
            domain = extract_domain(url)
            if domain in domain_counts:
                domain_counts[domain].add(url)
            else:
                domain_counts[domain] = {url}

        # Prints a list of how many of which domain has been scanned
        file.write(f"\n\nScanned Domains ({len(domain_counts)}):\n\n")
        sorted_domains = sorted(domain_counts.items(), key=lambda x: len(x[1]), reverse=True)
        for domain, urls in sorted_domains:
            file.write(f"{domain} - {len(urls)} URLs\n")

    print(f"File Saved under: {filename}")
