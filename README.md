# CopyrightArmor
<p style="text-align: center">The only Open Source Tool to fight against piracy.</p>

**CopyrightArmor** is a tool that scans and detects for pirated content for special research or to takedown. We aim for decentralisation and independence of DMCA Reporting Agencies.

# Features
- **Detecting Stolen Images**: CopyrightArmor detects stolen images by matching sha256 "hashes"
- **Detecting Stolen Files**: CopyrightArmor detects stolen files by matching sha256 "hashes"
- **Web Scraping Engine**: CopyrightArmor uses a robust web scraping engine to crawl and analyze websites for potentially infringing content.
- **Recursive Scrapping**: Recursively scans websites.
- **Google Optimized**: by using `--google` and `--google-search` without `-url` the web scraping engine will be optimized for Google Search.
- **Google SERP Engine**: CopyrightArmor detects most of pirate sites on the Google Search results. ([always check for false positives](https://github.com/Copy05/CopyrightArmor/discussions/4))
- **Flexible**: You can configurate how and what type of links it should scrape:
    - Exclude Social Media Links
    - Exclude Query parameter links
    - Exclude External Links
- **Generate DMCA Takedown Letters**: by using `create-report.py` inside the `report` directory.
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

4. Open up `src/hashes.json` and add all content that you want to scan for and use this syntax:

**`--google-search`** scans only for the content inside `"entertainment"`
```json
{
    "images": [
        {
            "original_url": "https://t3.ftcdn.net/jpg/05/41/71/02/360_F_541710260_3qZwn627nHyHA99xIktU7tKotn93YGjw.jpg",
            "copyright_owner": "Example Corp.",
            "hash": "3b99f49776f433aeb000fa010e452879198fe4be7f6660552527b53304268342",
            "description": "A Pink Cherry Tree"
        },
    ],
    "files": [
        {
            "original_url": "https://t3.ftcdn.net/jpg/05/41/71/02/361_F_541710260_3qZwn627nHyHA99xIktU7tKotn93YGjw.exe",
            "copyright_owner": "Example Corperation.",
            "hash": "3b99f49776f433aeb000fa010e452879198fe4be7f6660552527b53304268343",
            "description": "Another Pink Cherry Tree Exe"
        }
    ],
    "entertainment": [
        {
            "title": "EntertainRewind 2024",
            "original_url": "example.com",
            "copyright_owner": "Entertainmasters",
            "hash": "c8392dc67d913d39664e0fc400280a2de03107348f7432e226194f0a7e4eeebe"
        }
    ]
}
```

# Contribution

I do accept contributions to this project. create a pull request and describe your changes !

# Most Targetted Copyright Owners

**To see how much piracy happened on the internet here is a graph:**

| Catagory              | URLs              |
|-----------------------|-------------------|
| MG Premium LTD (Aylo) | +1,092,671,418    |
| Music                 | +742,100,209      |
| Movies / Television   | +741,019,179      |
| Webtoons              | +711,855,406      |
| Anime                 | +443,879,761      |
| Manga                 | +195,188,170      |
| Models                | +167,086,838      |
| XXX                   | +11,971,422       |
| WGCZ (BangBros)       | +11,355,801       |