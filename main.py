from datetime import datetime
import os
import subprocess
import sys
import time
import requests # If we want to do any preliminary internet connection testing

import AI_Tools # Local interface with Meta AI
import Scraper # Local interface with Beautifuls Soup

first_name, last_name = "", ""

data_from_user = [
    ""
]
    
def invokeSherlock(possible_usernames):

    print( ("\033[90m {}\033[00m" .format(f"\n[*] Assembling username queries...")) )


    # Arguments that are always passed to Sherlock
    sherlock_query = [
        "sherlock", # Calls Sherlock from the CLI
        "-v", # Verbose, aka show debug info
        # "--no-color", # Disable color output (consider changing)
        # "--no-txt", # Stops creation of txt output files (does not exist in this version)
        # "--csv", # Makes CSV files in addition to the .txt
        "--timeout", "5",
        "--folderoutput", "results",
        "--site", "Reddit",
        "--site", "Twitter",
        "--site", "Instagram",
    ]
   
    print( ("\033[90m {}\033[00m" .format(f"\n[*] Ready. Starting Sherlock...")) )

    # Assemble the query with the usernames
    for entry in possible_usernames:
        sherlock_query.append(entry)
    
    # Pass the sherlock_query to the CLI
    subprocess.run(sherlock_query)

    # Read the .txt files that are written by Sherlock
    new_array = []
    for entry in possible_usernames:
        if os.path.exists(f"results/{entry}.txt"):
            with open(f"results/{entry}.txt") as file:
                for temp in file:
                    if temp.startswith("http"):
                        new_array.append(temp.replace('\\n', ''))

    for entry in new_array:
        print( ("\033[95m {}\033[00m" .format(f"{entry}")) )

    # Returns array of URLs to each account that exists on each site 
    return new_array

def getUsernames(passed_username):
    global data_from_user
    specific_usernames = ""
    mode = "default"

    # prompt for username (skip if passed username(s))
    if not passed_username:
        print("[*] Do you know any of the username(s) you want to check? Type 'yes' Otherwise press ENTER.")
        if input() == 'yes':
            print("[*] Please enter the USERNAME. If there is more than one, seperate each one by a comma:")
            specific_usernames = input().strip().split(',')
            print(specific_usernames)
        elif not specific_usernames:
            print( ("\033[91m {}\033[00m" .format(f"! NO USERNAMES PROVIDED !")) )
        mode = "username"

    # prompt for first and last name
    print("[*] Please enter the Person's FIRST NAME:")
    first_name = input()
    print("[*] Please enter the Person's LAST NAME:")
    last_name = input()
    
    # prompt for additional information to aid in username and password generation
    if mode == "username":
        print( ("\033[93m {}\033[00m".format(f"~Username Mode~")) )
        print(f"[*] Enter identifiable information about {first_name} {last_name}.\n    This information will be used to generate possible USERNAMES and PASSWORDS.")
    else:
        print( ("\033[93m {}\033[00m".format(f"~Default Mode~")) )
        print(f"[*] Enter identifiable information about {first_name} {last_name}.\n    This information will be used to generate possible PASSWORDS.")

    print(f"\tInclude information regarding their identity such as,\n\tcontact information, residences, places of employment,\n\tfamily member names, pet names or animal type,\n\thobbies, interests, favorite colors or numbers,\n\tetceterea...")
    
    # Pass some already defined data to the LLM for context
    data_from_user.append(f"My name is {first_name} {last_name}.")
    if(specific_usernames):
        data_from_user.append(f"I already have some usernames already: {specific_usernames}. Please do not change them but put them at the top of your list that you give me.")

    # Collect multiple lines of input to be passed to the LLM
    while True:
        user_input = input()
            
        if user_input == "done":
            break

        data_from_user.append(f"{user_input}, ")

    # Return list of usernames that were passed through the CLI. No new usernames are generated.
    if mode == "default":
        return [i.strip() for i in passed_username.split(',')]

    print( ("\033[92m {}\033[00m" .format(f"\n[*] Retrieving possible aliases for, {first_name} {last_name}...")) )

    # Check to see if 
    possible_usernames= AI_Tools.genUsernames(data_from_user)
    if possible_usernames.startswith("ERROR"):
        print( ("\033[95m {}\033[00m" .format(f"{possible_usernames}")) )
        sys.exit(-1)
    else:
        possible_usernames = [i.strip() for i in possible_usernames.split(',')]

    if not specific_usernames == None:
        for index in range(len(specific_usernames)):
            if not specific_usernames[index] == specific_usernames[index]:
                possible_usernames.append(specific_usernames[index])

    while possible_usernames and " " in possible_usernames[-1]:
        possible_usernames.pop()

    return possible_usernames

def getPasswords(list_of_links):

    query_to_passwords = []

    print( ("\033[93m {}\033[00m" .format(f"~Password Mode~")) )

    # Pass some already defined data to the LLM for context
    if not data_from_user == None:
        query_to_passwords.append(data_from_user)
    query_to_passwords.append(f"Here are the websites that I frequently use, in case it helps you. {list_of_links}")

    print("")
    possible_passwords = []
    count = len(list_of_links)
    
    
    for entry in list_of_links:
        print( ("\033[92m {}\033[00m" .format(f"[+]Generating password solutions for {entry}{count}[*] sites left.")) )
        query_to_passwords.append(Scraper.GetPageMetaData(entry,data_from_user))
        time.sleep(3) # sleep to avoid throttling by meta
        count = count - 1

    LLM_response = AI_Tools.genPasswords(query_to_passwords)
    possible_passwords = LLM_response

    print(f"Password generation complete!")

    # Returns a list of passwords
    return possible_passwords

def buildAttackList(target_websites, target_passwords):
    print("[*]",end="")
    print( ("\033[92m {}\033[00m" .format(f"Building attack profiles for {last_name}, {first_name}...")) )

    # target_passwords = [i.strip() for i in target_passwords.split(',')]

    attack_list = []

    for site in target_websites:
        for pword in target_passwords:
            attack_list.append([site, pword])
    
    for entry in attack_list:
        print(entry)

    print("\033[91m {}\033[00m" .format("\n\n\t\t ATTACK PROFILE READY \n\n"))
    print("[*] Press ENTER to save results.")
    input()
    
    print(f"[*] Saving to Disk...")

    dt = datetime.now().strftime("%c")

    path_to_output = f"results/Attack_List_{dt.replace(' ', '_').replace(':', '_')}.csv"
    results_file = open(path_to_output, "a")
    for entry in attack_list:
        results_file.write(str(entry))
    
    print(f"[*] {dt.replace('_', ' ').replace(':', '_')} Created file. \n\nTry: \"cat {path_to_output}\"")

def main():
    global first_name
    global last_name
    passed_user_name = ""

    if len(sys.argv) >= 2:
        if sys.argv[1] == "--help":
            print(f"usage: \"path\\to\\python\" \"path\\to\\scripty.py [arguments:optional]\n\n\tOptional Arguments:\n\t--help\t\tprints the usage information(this message)\n\t[USERNAME]\ta username with no spaces to skip username mode\n\t\t*You will NOT be prompted for more entries*\n\nStill having trouble? Try: \"pip install --user sherlock-project\"")
            sys.exit(0)
        else:
            for i in sys.argv[1:]:
                passed_user_name = i

    try:

        possible_usernames = getUsernames(passed_user_name)
        sites_to_attack = invokeSherlock(possible_usernames)
        possible_passwords = getPasswords(sites_to_attack)

        buildAttackList(sites_to_attack, possible_passwords)

    except KeyboardInterrupt:
        print( ("\033[90m {}\033[00m" .format(f"\n.\n[*] Program terminated. Exiting...")) )        

if __name__ == '__main__':
    main()
