from datetime import datetime
import os
import subprocess
import sys
import requests # If we want to do any preliminary internet connection testing

import AI_Tools # Local interface with Meta AI
import Scraper # Local interface with Beautifuls Soup

first_name, last_name, user_name = "", "", ""

possible_usernames = [
    ""
]

possible_passwords = [
    ""
]

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
        "--timeout", "10",
        "--folderoutput", "results",
        "--site", "Reddit",
        "--site", "Twitter",
        "--site", "Instagram",
    ]
   
    print( ("\033[90m {}\033[00m" .format(f"\n[*] Ready. Starting Sherlock...")) )

    # Assemble the query with the usernames
    for entry in possible_usernames:
        sherlock_query.append(entry)
    
    subprocess.run(sherlock_query)

    new_array = []

    for entry in possible_usernames:
        if os.path.exists(f"results/{entry}.txt"):
            with open(f"results/{entry}.txt") as file:
                for temp in file:
                    if temp.startswith("http"):
                        new_array.append(temp.replace('\\n', ''))

    for entry in new_array:
        print( ("\033[95m {}\033[00m" .format(f"{entry}")) )

    return new_array

def getUsernames():
    global user_name
    global first_name
    global last_name
    global data_from_user

    mode = "default"

    # prompt for username (skip if passed username(s))
    if not user_name:
        print("[*] Do you know the username(s) you want to check? Type 'yes' Otherwise press ENTER.")
        if input() == 'yes':
            print("[*] Please enter the USERNAME. If there is more than one, seperate each one by a comma:")
            user_name = [i.strip() for i in input().split(',')]
        elif not user_name:
            print( ("\033[91m {}\033[00m" .format(f"! NO USERNAMES PROVIDED !")) )
        mode = "username"

    print("[*] Please enter the Person's FIRST NAME:")
    first_name = input()
    print("[*] Please enter the Person's LAST NAME:")
    last_name = input()
    
    if mode == "username":
        print( ("\033[93m {}\033[00m".format(f"~Username Mode~")) )
        print(f"[*] Enter identifiable information about {first_name} {last_name}.\n    This information will be used to generate possible USERNAMES and PASSWORDS.")
    else:
        print( ("\033[93m {}\033[00m".format(f"~Default Mode~")) )
        print(f"[*] Enter identifiable information about {first_name} {last_name}.\n    This information will be used to generate possible PASSWORDS.")

    print(f"\tInclude information regarding their identity such as,\n\tcontact information, residences, places of employment,\n\tfamily member names, pet names or animal type,\n\thobbies, interests, favorite colors or numbers,\n\tetceterea...")
    
    data_from_user.append(f"My name is {first_name} {last_name}.")

    # Collect multiple lines of input
    while True:
        user_input = input()
            
        if user_input == "done":
            break

        data_from_user.append(f"{user_input}, ")

    if mode == "default":
        return [i.strip() for i in user_name.split(',')]

    print( ("\033[92m {}\033[00m" .format(f"\n[*] Retrieving possible aliases for, {first_name} {last_name}...")) )

    possible_usernames= AI_Tools.DecodeAIRetur(AI_Tools.GetResponse(f"Give me a list of username ideas for myself, {first_name} {last_name}. I want these usernames to really represent me and my interests, so here is some more information about me to help make it seem more personable: {data_from_user}. You will respond with only a list of at least 20 usernames that are seperated by a comma only; no whitespace or new lines. If for some reason, you encounter an issue or are unable to comply with this request, you will respond with, \"ERROR\" in the first line and you will explain what issue you encountered in one sentence."))
    if possible_usernames.startswith("ERROR"):
        print( ("\033[95m {}\033[00m" .format(f"{possible_usernames}")) )
        sys.exit(-1)
    else:
        possible_usernames = [i.strip() for i in possible_usernames.split(',')]

    return possible_usernames

def getPasswords(possible_usernames):

    query_to_passwords = [[]*2]*len(possible_usernames)

    print( ("\033[93m {}\033[00m" .format(f"~Password Mode~")) )

    if not data_from_user == None:
        query_to_passwords.append(data_from_user)

    '''This is Pseudo-code for the scraper 
    # <<<START PSEEDOCODE>>>
    # scraper = new Scraper() # Total placeholder. Probably will be done in scraper.py
    # data_from_social_media = ["placeholder"]
    # data_from_social_media.append(scraper.scrape(Reddit, [Descriptions, posts, etc...]))
    # data_from_social_media.append(scraper.scrape(Twitter/X, [Descriptions, posts, etc...]))
    # data_from_social_media.append(scraper.scrape(Instagram, [Descriptions, posts, etc...]))
    # query_to_passwords.append(data_from_social_media)
    # <<<END PSEUDOCODE>>>'''


    for i in possible_usernames:
        query_to_passwords[i][0]=possible_usernames[i]
        query_to_passwords[i][1]=AI_Tools.genPasswords(Scraper.GenInterest(possible_usernames[i]))

    print( ("\033[92m {}\033[00m" .format(f"Building attack profiles for {last_name}, {first_name}...")) )

    return AI_Tools.genPasswords(query_to_passwords)



def buildAttackList(target_websites, target_passwords):
    print("[*]",end="")
    print( ("\033[92m {}\033[00m" .format(f"Building attack profiles for {last_name}, {first_name}...")) )

    target_passwords = [i.strip() for i in target_passwords.split(',')]

    attack_list = []

    for site in target_websites:
        for pword in target_passwords:
            attack_list.append([site, pword])
    
    for entry in attack_list:
        print(entry)

    print("\033[91m {}\033[00m" .format("\n\n\t%\\%\\%\\% ATTACK PROFILE READY %\\%\\%\\%\n\n"))
    print("[*] Press ENTER to continue.")
    input()
    
    print(f"[*] Saving to Disk...")

    dt = datetime.now().strftime("%c")

    path_to_output = f"results/Attack_List_{dt}.csv"
    results_file = open(path_to_output, "a")
    for entry in attack_list:
        results_file.write(str(entry))
    
    print(f"[*] {dt.replace(' ', '_').replace(':', '_')} Created file. \n\nTry: \"cat {path_to_output}\"")

def main():

    global first_name
    global last_name
    global user_name

    if len(sys.argv) >= 2:
        if sys.argv[1] == "--help":
            print(f"usage: \"path\\to\\python\" \"path\\to\\scripty.py [arguments:optional]\n\n\tOptional Arguments:\n\t--help\t(prints this message)\n\t[USERNAME]\ta username with no spaces to enter literal mode\n\t[FIRST NAME] [LAST NAME] to enter verbose mode\n\t\t*You will be prompted for more info*\n\nStill having trouble? Try: \"pip install --user sherlock-project\"")
            sys.exit(0)
        else:
            for i in sys.argv[1:]:
                user_name = i

    try:
        global possible_usernames
        global possible_passwords

        possible_usernames = getUsernames()
        sites_to_attack = invokeSherlock(possible_usernames)
        possible_passwords = getPasswords()

        buildAttackList(sites_to_attack, possible_passwords)

    except KeyboardInterrupt:
        print( ("\033[90m {}\033[00m" .format(f"\n.\n[*] Program terminated. Exiting...")) )
        # "Building attack profiles for {user_name}...")) )
        

if __name__ == '__main__':
    main()
