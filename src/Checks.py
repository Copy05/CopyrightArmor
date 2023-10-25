#
# (c) Copyright Copy05, 2023
#
# Checks.py | Checks for given parameters and valid URLs
#

from urllib.parse import ParseResult
from colorama import Style, Fore

class Checks:
    @staticmethod
    def ExcludePaths(Verbose : bool, ExcludePath : str, Visted_URLs : set) -> set:
        v_u = Visted_URLs
        print("Adding URLs from: ", ExcludePath)
        with open(ExcludePath, 'r') as file:
            for line in file:
                cleanline = line.strip()
                if Verbose:
                    print("Add URL: ", cleanline)
                v_u.add(cleanline)
        return v_u
    
    @staticmethod
    def InvalidHttp(original_url : str, URL : str, Verbose : bool) -> bool:
        if URL.scheme != 'http' and URL.scheme != 'https':
            if Verbose:
                print(Fore.YELLOW, f"Skipped URL with invalid scheme: {original_url}")
                print(Style.RESET_ALL)
            return True
        else:
            return False

    @staticmethod
    def QueryParameter(original_url : str, URL : ParseResult, DeepSearch : bool, Verbose: bool) -> bool:
        if not DeepSearch and URL.query:
            if Verbose:
                print(Fore.YELLOW, f"Skipped URL with query parameters: {original_url}")
                print(Style.RESET_ALL)
            return False
        else:
            return True
