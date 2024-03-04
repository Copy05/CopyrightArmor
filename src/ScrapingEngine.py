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

from colorama import Fore, Style

def AddToQueue(next_url):
    from Scrape import visited_urls, TheQueue, Found_Links, FoundLinkCount

    if next_url not in visited_urls and next_url not in TheQueue.queue:
        TheQueue.put(next_url)
        Found_Links.add(next_url)
        FoundLinkCount += 1

def FilterLinks(next_url, verbose, IncludeSocials):
    from Scrape import Socials

    if next_url.startswith("javascript:") or next_url.startswith("mailto:") or next_url.startswith("tel:"):
        if verbose:
            print(Fore.YELLOW, f"Skipping {next_url} because these types of links arent allowed")
            print(Style.RESET_ALL)
        return True

    if IncludeSocials is False:
        if any(next_url.startswith(social_link) for social_link in Socials):
            if verbose:
                print(Fore.YELLOW, f"Skipping {next_url}.")
                print(Style.RESET_ALL)
            return True
        
    return False