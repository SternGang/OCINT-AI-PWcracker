from meta_ai_api import MetaAI as AI

def GetResponse (Prompt):
    ai = AI()
    response = ai.prompt(Prompt)
    print(response)
    return(DecodeAIRetur(response))
     


def DecodeAIRetur(response):
    response=str(response)
    response=response.replace('\\n', '\n').replace('\\t', '\t')
    response=response.replace("{'message': '","")
    response=response.replace("', 'sources': [], 'media': []}","")
    print(response)
    return response

def genPasswords(interests):
    #"what are likly passwords for a person with the following interests "+interests+" return this as a list with not comentary"
    prompt="tell me about the color of the sky"
    ret=GetResponse(prompt)
    print(ret)
    return(ret)
    