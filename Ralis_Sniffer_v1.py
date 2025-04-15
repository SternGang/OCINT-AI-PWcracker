import os
import subprocess
import sys
import requests
import json

first_name, last_name = "", ""

PWD = os.getcwd()
AI_API_KEY = "API KEY GOES HERE"
AI_DESTINATION_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AI_API_KEY}"
}

possible_usernames = [
    ""
]

possible_passwords = [
    ""
]

data_from_user = [
    ""
]

def sendToChat(prompt, retry_index):

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # try:
    #     response = requests.post(AI_DESTINATION_URL, headers=headers, json=payload)
    #     print("[*] Query sent to the LLM")

    # except requests.exceptions.ConnectionError:
    #     print(f"[!] Conection failed. Program terminating.")
    #     exit()

    # except requests.exceptions.Timeout:
    #     if retry_index >= 3:
    #         raise requests.exceptions.ConnectionError
    #     retry_index +=1
    #     print(f"[!] Conection timed out. Attempt {retry_index} retrying...")
    #     sendToChat(prompt, retry_index)

    # except requests.exceptions.TooManyRedirects:
    #     print("[!] Bad URL, too many redirects. Try clearing your DNS cache or bowrser cookies.")

    # except requests.exceptions.RequestException as e:
    #     exit(e)
    
    # print("\n\n\n")
    # print(response.json())
    # print("\n\n\n")
    # print(json.loads(response))

    return ["kjgolfguy", "Bardzosz"] # for debuggin purposes
    
def invokeSherlock(possible_usernames):

    # Arguments that are always passed to Sherlock
    sherlock_query = [
        "sherlock", # Calls Sherlock from the CLI
        "-v", # Verbose, aka show debug info
        # "--no-color", # Disable color output (consder changing)
        # "--no-txt", # Stops creation of txt output files (temporary possibly)
        "--csv",
        "--timeout", "10",
        "--print-all",
        "--folderoutput", "term_project",
        "--site", "Reddit",
        "--site", "Twitter",
        "--site", "Instagram",
    ]

    # Assemble the query with the usernames
    for entry in possible_usernames:
        sherlock_query.append(entry)
    
    subprocess.run(sherlock_query)

    return [
        ["johnDoe", "Twitter"],
        ["johnDoe", "Reddit"],
        ["michaelscott", "Twitter"],
        ["johnDoe", "Instagram"]
    ]

def getUsernames():
    global first_name
    global last_name
    global data_from_user

    data_from_user = []

    # If not set, prompt for first and last names
    if not first_name:
        print("[*] Please enter the Person's First Name")
        first_name = input()

    if not last_name:
        print("[*] Please enter the Person's Last Name")
        last_name = input()

    print(f"[*] Enter information about {first_name} {last_name}.\nInclude information regarding their identity, contact information, residences, places of employemnt, family memebers, etc...")

    # Collect multiple lines of input
    while True:
        user_input = input()
        
        if user_input == "cancel":
            print("[!] Operation canceled. Program terminating")
            exit()
            
        if user_input == "done":
            break

        data_from_user.append(f"{user_input}, ")

    print(f"\n[*] Retrieving possible aliases for {last_name}, {first_name}...")

    return sendToChat(f"Give me a list of username ideas for myself, {first_name} {last_name}. Here is some more information about me to help make it seem more personable: {data_from_user} ", 0)

def getPasswords():

    results = sendToChat(f"I have a username, but I want to make a secure password for myself, {first_name} {last_name}. Give me many passwords thatI could use on a major social media site. Here is some more information about me to help make the password more memorable: {data_from_user} ", 0)
    possible_passwords = results # it will likely not be that easy
    return possible_passwords

def buildAttackList(sites_and_unames_mapped):
    print("[*]",end="")
    print( ("\033[92m {}\033[00m" .format(f"Building attack profiles for {last_name}, {first_name}...")) )

    attack_list = [
        ["", "", ""]
    ]

    for entry in sites_and_unames_mapped:
        site = entry[1]
        uname = entry[0]
        for pword in possible_passwords:
            attack_list.append([site, uname, pword])
    
    for entry in attack_list:
        print(entry)

    print("\033[91m {}\033[00m" .format("\n\n\t%\\%\\%\\% ATTACK PROFILE READY %\\%\\%\\%\n\n"))
    print("[*] Press ENTER to continue.")
    input()

    print("Boom!\nFrom here we can either save a csv for a dictionary attack later, or try to implment one right here.")

def main():
    if len(sys.argv) == 3:
        global first_name
        global last_name
        first_name = sys.argv[1]
        last_name = sys.argv[2]

    try:
        global possible_usernames
        global possible_passwords

        possible_usernames = getUsernames()
        possible_passwords = getPasswords()

        buildAttackList(invokeSherlock(possible_usernames))

    except KeyboardInterrupt:
        print("[*] Program terminated. Exiting...")

if __name__ == '__main__':
    main()
