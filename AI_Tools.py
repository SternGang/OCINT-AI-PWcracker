from meta_ai_api import MetaAI as AI

def GetResponse (Prompt):
    ai = AI()
    response = ai.prompt(Prompt)
    return(DecodeAIRetur(response))
     


def DecodeAIRetur(response):
    response=str(response)
    response=response.replace('\\n', '\n').replace('\\t', '\t')
    response=response.replace("{'message': '","")
    response=response.replace("', 'sources': [], 'media': []}","")

    return response

def genPasswords(interests):
    prompt="what are likly passwords for a person with the following interests "+interests+" return this as a list with not comentary"
    ret=GetResponse(prompt)
    return(ret)
    