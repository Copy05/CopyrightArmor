# CopyrightArmor
<p style="text-align: center">The only Open Source Tool to fight against piracy.</p>

**CopyrightArmor** is a tool that scans and detects for pirated content for special research or to takedown. We aim for decentralisation and independence of DMCA Reporting Agencies.

# Features
- **Web Scraping Engine**: CopyrightArmor uses a robust web scraping engine to crawl and analyze websites for potentially infringing content.
- **Recursive Scrapping**: Recursively scans websites.
- **Google Optimized**: by using `--google` the scraping engine will be optimized for Google Search
- **Flexible**: You can configurate how and what type of links it should scrape:
    - Exclude Social Media Links
    - Exclude Query parameter links
    - Exclude External Links
- **Detailed Reports**: Generate detailed reports of scanned URLs and domain statistics to keep records of your scanning activities:
```
CopyrightArmor 10/30/23 Report

Scanned URLs (5):
https://www.iana.org/domains/example
https://example.com
https://www.iana.org/protocols
https://www.iana.org/domains
https://www.iana.org/

Scanned Domains (2):
www.iana.org - 4 URLs
example.com - 1 URLs
```
Even more detailed with the `--detailed-report` argument

# Installations

1. Clone the CopyrightArmor repository from GitHub:
```
git clone https://github.com/Copy05/CopyrightArmor.git
```

2. Navigate to the project directory:
```
cd CopyrightArmor
```

3. Install the required dependencies using pip:
```
pip install -r requirements.txt
```

# Most Targetted Copyright Owners

**To see how much piracy happened on the internet here is a graph:**

| Catagory              | URLs         |
|-----------------------|--------------|
| MG Premium LTD (Aylo) | +992,671,418 |
| Music                 | +742,100,209 |
| Movies / Television   | +741,019,179 |
| Webtoons              | +711,855,406 |
| Anime                 | +443,879,761 |
| Manga                 | +195,188,170 |
| Models                | +167,086,838 |
| XXX                   | +11,971,422  |
| WGCZ (BangBros)       | +11,355,801  |
