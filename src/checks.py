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
