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

import os
import json

from datetime import datetime
from colorama import Fore, Back, Style, init

def Load_Default_Letter():

    try:
        with open("settings.json", "r") as file:
            settings_data = json.load(file)
            letter_content = settings_data.get("LetterContent", "")
            return letter_content
    except FileNotFoundError:
        print("Error: 'settings.json' file not found.")
        return ""
    except json.JSONDecodeError:
        print("Error: Unable to parse 'settings.json'. Make sure it is a valid JSON file.")
        return ""
    
    
def Load_Company():

    try:
        with open("settings.json", "r") as file:
            settings_data = json.load(file)
            company = settings_data.get("CompanyName", "")
            return company
    except FileNotFoundError:
        print("Error: 'settings.json' file not found.")
        return ""
    except json.JSONDecodeError:
        print("Error: Unable to parse 'settings.json'. Make sure it is a valid JSON file.")
        return ""
    

def Load_Agency():

    try:
        with open("settings.json", "r") as file:
            settings_data = json.load(file)
            agency = settings_data.get("AgencyName", "")
            return agency
    except FileNotFoundError:
        print("Error: 'settings.json' file not found.")
        return ""
    except json.JSONDecodeError:
        print("Error: Unable to parse 'settings.json'. Make sure it is a valid JSON file.")
        return ""


def GetDate():
    return datetime.now().strftime("%Y-%m-%d")


def CreateMenu(options):

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        try:
            choice = int(input(f"{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}Enter the number of your choice: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}"))
            print(f"{Style.RESET_ALL}", end="")
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            

def GetColoredInput(prompt):

    init(autoreset=True)

    colored_prompt = f"{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}{prompt}: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}"

    input_text = input(colored_prompt)

    print(f"{Style.RESET_ALL}", end="")

    return input_text


def input_with_default(prompt, default):
    user_input = input(f"{prompt} ({default}): ")
    return user_input + ".txt" if user_input else default


def generate_unique_filename(base_name, extension):
    count = 1
    file_name = f"{base_name}{extension}"

    while os.path.exists(file_name):
        count += 1
        file_name = f"{base_name}-{count}{extension}"

    return file_name


def Confirmation(prompt, yes_text, no_text):
    init(autoreset=True)
    
    while True:
        response = input(f"{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}{prompt}{Style.RESET_ALL}\n{Fore.LIGHTCYAN_EX}[Y] {yes_text}\t\t{Fore.LIGHTRED_EX}[N] {no_text}\n{Style.RESET_ALL}")
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


def SaveReport(file_name, letter_contents):
    try:
        base_name, extension = os.path.splitext(file_name)
        count = 1

        while os.path.exists(file_name):
            count += 1
            file_name = f"{base_name}-{count}{extension}"

        file_path = os.path.join(os.getcwd(), file_name)

        with open(file_path, "w") as file:
            file.write(letter_contents)

        print(f"Report saved successfully to: {file_path}")
    except Exception as e:
        print(f"Error saving report: {e}")


def ClearTerminal():

    os.system('cls' if os.name == 'nt' else 'clear')


def FormatText(input_text, company, product, infringer, agency):

    formatted_text = input_text.replace("{companyName}", company)
    formatted_text = formatted_text.replace("{agencyName}", agency)
    formatted_text = formatted_text.replace("{productName}", product)
    formatted_text = formatted_text.replace("{infringerName}", infringer)
    formatted_text = formatted_text.replace("\\n", "\n")

    return formatted_text


def CustomLetterContents(copyright_owner, infringer, product, agency=""):
    
    lt = '{'
    rt = "}"

    print(f"""
Write the contents of the letter. the letter can contain placeholders that will be automatically converted to their properties.

{Style.BRIGHT}SYNTAX{Style.RESET_ALL}:
\t{Fore.LIGHTRED_EX}{lt}companyName{rt}{Style.RESET_ALL} - The Company who owns the Copyright.
\t{Fore.LIGHTRED_EX}{lt}productName{rt}{Style.RESET_ALL} - The Product name.
\t{Fore.LIGHTRED_EX}{lt}infringerName{rt}{Style.RESET_ALL} - The Name/Company of the Infringer.
\t{Fore.LIGHTRED_EX}\\n{Style.RESET_ALL} - New Character.
{f"{Fore.LIGHTRED_EX}{lt}agencyName{rt}{Style.RESET_ALL} - The DMCA Agency that works for the copyright owner." if agency else ""}

{Style.BRIGHT}YOUR SUBMITTED DATA{Style.RESET_ALL}:
\t{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}Copyright Owner: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{copyright_owner}{Style.RESET_ALL}
\t{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}Copyright Infringer: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{infringer}{Style.RESET_ALL}
\t{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}Product: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{product}{Style.RESET_ALL}
{f"{Fore.LIGHTYELLOW_EX}{Back.RESET}{Style.BRIGHT}Agency Name: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{agency}{Style.RESET_ALL}" if agency else ""}
""")