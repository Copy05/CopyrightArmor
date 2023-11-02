from colorama import Style, Fore
from urllib.parse import urljoin

def PrintFoundLinks(original_url : str, link):
        print(Fore.YELLOW, f"Anchor Tag: {urljoin(original_url, link['href'])}")
        print(f"Anchor Text: {link.text.strip()}")
        print(Style.RESET_ALL)