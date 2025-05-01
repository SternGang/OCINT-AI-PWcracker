from meta_ai_api import MetaAI as AI
import time

def GetResponse (Prompt):
    
    

    response = ai.prompt(Prompt)
    

    return(DecodeAIRetur(response))
     


def GetResponse(prompt, retries=3, delay=5):
    ai = AI()
    print( ("\033[90m {}\033[00m" .format(f"\n[*] Querying LLM for solutions...")) )
    for i in range(retries):
        try:
            response = ai.prompt(prompt)
            print( ("\033[90m {}\033[00m" .format(f"\n[*] Response received!")) )
            if response:
                return DecodeAIRetur(response)
        except Exception as e:
            print("\033[91m {}\033[00m" .format(f"[!] AI call failed. FACEBOOK IS THROTTLING YOU: {e}") )
            print("\033[91m {}\033[00m" .format(f"[*] Retrying in {delay}s...") )

        time.sleep(delay * (10 ** i))  # exponential backoff
    print("\033[91m {}\033[00m" .format(f"[!] Meta API call unsuccseful. Exiting.") )

    return None



def DecodeAIRetur(response):
    response=str(response)
    response=response.replace('\\n', '\n').replace('\\t', '\t')
    response=response.replace("{'message': '","")
    response=response.replace("', 'sources': [], 'media': []}","")

    return response

def genPasswords(interests):
    prompt= f"I want to make some memorable passwords that have some connection to me and my interests, so here is my name and some information about me to help make it seem more personable: {interests}. You will respond with only a list of at least 100 passwords that are seperated by a comma only; no whitespace or new lines. Make the passwords rangeing in different levels of security from simple to more complex passwords while still relating to my interests fully. If for some reason, you encounter an issue or are unable to comply with this request, you will respond with, \"ERROR\" in the first line and you will explain what issue you encountered in one sentence. Do not add any other text at the end of the message. I understand that you are not perfect with different langauges. "
    ret=GetResponse(prompt)
    PWarray = ret.split(",")
    return(PWarray)

def genUsernames(interests):
    prompt= f"Give me a list of username ideas for myself. I want these usernames to really represent me and my interests, so here is some more information about me to help make it seem more personable: {interests}. You will respond with only a list of at least 20 usernames that are seperated by a comma only; no whitespace or new lines. If for some reason, you encounter an issue or are unable to comply with this request, you will respond with, \"ERROR\" in the first line and you will explain what issue you encountered in one sentence. Do not add any other text at the end of the message. I understand that you are not perfect with different langauges. "
    ret=GetResponse(prompt)
    return(ret)
    
