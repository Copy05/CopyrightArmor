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

import argparse
from colorama import Style, Fore
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

    parser.add_argument("-ver", "--version", action="store_true", help="Print the version information")
    parser.add_argument("-url", "-link", "--site", help="specifies the URL of the piracy website to scan. This option can be used multiple times to specify multiple websites.")
    parser.add_argument("--report-file", action="store_true", help="Specify if there should be a report file when exiting")
    parser.add_argument("--rate-limit", action="store_true", help="Set a rate limit for requests (requests per second) to avoid overloading websites.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Increase verbosity for debugging purposes.")
    parser.add_argument("--debug", action="store_true", help="Enables Debug Informations for Debug purposes")
    parser.add_argument("--file-types", help="Specify file types/extensions to look for (e.g., .mp3, .mp4, .pdf).")
    parser.add_argument("--keyword", help="Provide keywords or phrases to identify pirated content.")
    parser.add_argument("--depth", "-d", type=int, help="Specify how deep the tool should crawl the website (number of levels).")
    parser.add_argument("--external-visits", "-ev", action="store_true", help="Enables visiting sites that's outside the original website")
    parser.add_argument("--deep-search", "-ds", action="store_true", help="Enables deep search which also includes query paramters (.*?*=*)")
    parser.add_argument("--include-socials", "-is", action="store_true", help="Allows Social Media Links to scan")
    parser.add_argument("--google", "-g", action="store_true", help="Optimizes the scraping engine for Google Search.")
    parser.add_argument("--google-search", help="Uses the Google Search Webscrapping engine.")
    parser.add_argument("--exclude", help="Specifies a text file with all URLs to Exclude")
    parser.add_argument("--ignore-ssl", "-no-ssl", action="store_true", help="Ignores all SSL Checks which may be unsecure in some sites.")

    args = parser.parse_args()

    if args.version:
        PrintVersion()

    if args.file_types:
        unimplemented_args = []
        if args.file_types:
            unimplemented_args.append("file_types")

        unimplemented_args_str = ", ".join(unimplemented_args)
    
        print(Fore.RED, f"ImplementationError: The argument(s) {unimplemented_args_str} is/are not implemented yet")
        print(Style.RESET_ALL)
        exit(1)

    if args.site:

        # To Avoid Long Execution Time when not using the scraping engine.
        from Scrape import ScrapeWebsite

        if not urlparse(args.site).scheme:
            args.site = "https://" + args.site

        ScrapeWebsite(args.site, depth=args.depth, RateLimmit=args.rate_limit, verbose=args.verbose, ExternalVisits=args.external_visits, 
                  DeepSearch=args.deep_search, ReportFile=args.report_file, ExcludePaths=args.exclude, IncludeSocials=args.include_socials, DebugInformation=args.debug, 
                  GoogleScrape=args.google, IgnoreSSL=args.ignore_ssl)


    if args.google and not args.site:

        # To Avoid Long Execution Time when not using the scraping engine.
        from GoogleScrape import GoogleScrape

        if args.detailed_report and args.report_file is False:
            print(Fore.RED, "Error: Invalid Argument: \"--detailed-report\" because \"--report_file\" is false")
            print(Style.RESET_ALL)
            exit(1)

        GoogleScrape(Query=args.google_search, RateLimmit=args.rate_limit, verbose=args.verbose, ReportFile=args.report_file)


    if not any(vars(args).values()):
        print(Fore.RED, "Error: No arguments provided. Use -h or --help for usage information.")
        print(Style.RESET_ALL)
        exit(1)
