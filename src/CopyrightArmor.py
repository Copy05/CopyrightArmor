import argparse
from colorama import Style, Fore
from Scrape import ScrapeWebsite
from urllib.parse import urlparse

def PrintVersion():
    print('''
CopyrightArmor v0.1
(c) Copy05 2022 - 2023
          
This tool is for scanning and monitoring for stolen content that you can take down.

URL: https://github.com/Copy05/CopyrightArmor
    ''')
    exit()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="The Free Tool to scan the websites for infringing content to take down")

    parser.add_argument("-monitor", action="store_true", help="Enable monitoring mode")
    parser.add_argument("-ver", "--version", action="store_true", help="Print the version information")
    parser.add_argument("-url", "-link", "--site", help="he URL of the piracy website to scan. This option can be used multiple times to specify multiple websites.")
    parser.add_argument("--report-file", action="store_true", help="Specify the report")
    parser.add_argument("--rate-limit", action="store_true", help="Set a rate limit for requests (requests per second) to avoid overloading websites.")
    parser.add_argument("--headless-browser", "--headless", help="Use a headless browser for website interaction and content detection.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Increase verbosity for debugging purposes.")
    parser.add_argument("--file-types", help="Specify file types/extensions to look for (e.g., .mp3, .mp4, .pdf).")
    parser.add_argument("--keyword", help="Provide keywords or phrases to identify pirated content.")
    parser.add_argument("--proxy", "-p", help="Use a proxy server for anonymized scanning (if necessary).")
    parser.add_argument("--user-agent", "-ua", help="Specify a custom User-Agent header for HTTP requests (to mimic different user agents).")
    parser.add_argument("--ignore-robots-txt", "--no-robots-txt", help="Ignore the 'robots.txt' file, which is used to control web crawlers.")
    parser.add_argument("--depth", "-d", help="Specify how deep the tool should crawl the website (number of levels).")
    parser.add_argument("--external-visits", "-ev", action="store_true", help="Enables visiting sites that's outside the original website")
    parser.add_argument("--deep-search", "-ds", action="store_true", help="Enables deep search which also includes query paramters (.*?*=*)")
    parser.add_argument("--exclude", help="Specifies a text file with all URLs to Exclude")

    args = parser.parse_args()

    if args.version:
        PrintVersion()

    if args.site:
        if not urlparse(args.site).scheme:
            args.site = "https://" + args.site

    ScrapeWebsite(args.site, RateLimmit=args.rate_limit, verbose=args.verbose, ExternalVisits=args.external_visits, 
                  DeepSearch=args.deep_search, ReportFile=args.report_file, ExcludePaths=args.exclude)


    if not any(vars(args).values()):
        print(Fore.RED, "Error: No arguments provided. Use -h or --help for usage information.")
        print(Style.RESET_ALL)
        exit(1)
