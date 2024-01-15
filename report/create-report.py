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