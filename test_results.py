import csv

# csv_file = 'tester1.csv' #put .csv file here

print("Enter the relative file path then press ENTER:")
csv_file = input()

search1 = 'YellowHorse2'
search2 = 'R3dL10n9!'  

with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    
    found = False
    for row_num, row in enumerate(reader, start=1):
        if any(search1 in cell for cell in row):
            print("Account is Compromised for Brent")
            found = True
        
        if any(search2 in cell for cell in row):
            print("Account is Compromised for Veronica")
            found = True

    if not found:
        print("All accounts are assumed Safe.")