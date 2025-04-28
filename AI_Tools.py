from meta_ai_api import MetaAI as AI

def GetResponse (Prompt):
    ai = AI()
    print( ("\033[90m {}\033[00m" .format(f"\n[*] Querying LLM for solutions...")) )

    response = ai.prompt(Prompt)
    print( ("\033[90m {}\033[00m" .format(f"\n[*] Response received!")) )

    return(DecodeAIRetur(response))
     


def DecodeAIRetur(response):
    response=str(response)
    response=response.replace('\\n', '\n').replace('\\t', '\t')
    response=response.replace("{'message': '","")
    response=response.replace("', 'sources': [], 'media': []}","")

    return response

def genPasswords(interests):
    prompt= f"I want to make some memorable passwords tha have some connection to me and my interests, so here is my name and some information about me to help make it seem more personable: {interests}. You will respond with only a list of at least 100 passwords that are seperated by a comma only; no whitespace or new lines. If for some reason, you encounter an issue or are unable to comply with this request, you will respond with, \"ERROR\" in the first line and you will explain what issue you encountered in one sentence."
    ret=GetResponse(prompt)
    return(ret)
    