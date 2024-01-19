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

from func import *

def main():

    default_company = Load_Company()
    agency = ""

    ClearTerminal()
    print("CopyrightArmor's DMCA Notice Report Creator.\n\n")

    
    print("How do you want your Company Name:")
    what_company = CreateMenu([f"Use Default Company Name (\"{default_company}\")", "Enter it myself"])

    if what_company == 1:
        copyright_owner = default_company
    elif what_company == 2:
        copyright_owner = GetColoredInput("Enter The Copyright Owner")

    if what_company == 2:
        ClearTerminal()
        print("Who does the claim:")
        what_agency = CreateMenu(["On our own behalf", "We're an agency"])

        if what_agency == 2:
            agency = GetColoredInput("Enter The Agency Name")


    ClearTerminal()
    infringer = GetColoredInput("Enter The Infringer")

    ClearTerminal()
    product = GetColoredInput("Enter The stolen copyrighted product")

    ClearTerminal()
    what_letter = CreateMenu(["Use Template from settings.json", "Custom"])

    if what_letter == 1:
        letter = Load_Default_Letter()
    elif what_letter == 2:
        ClearTerminal()
        CustomLetterContents(copyright_owner, infringer, product, agency)
        letter = input()

    ClearTerminal()
    letter = FormatText(letter, copyright_owner, product, infringer, agency)

    print(letter)
    confirm = Confirmation("Do you want to save your letter?", "Save", "Don't Save")

    if confirm == 1:
        ClearTerminal()
        filtered_company_name = copyright_owner.replace(" ", "-")
        default_filename = generate_unique_filename(f"{GetDate()}-{filtered_company_name}", ".txt")
        filename = input_with_default("Enter the filename", default_filename)
        SaveReport(filename, letter)
        ClearTerminal()
        exit()
    elif confirm == 2:
        ClearTerminal()
        exit()

if __name__ == "__main__":
    main()