from llm.api import call_llm

def llm_loop():
    print("Welcome! Please enter your query:")
    while True:    
        query = input()
        response = call_llm(query)
        print(response)