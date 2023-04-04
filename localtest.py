#Note: The openai-python library support for Azure OpenAI is in preview.
import os
from dotenv import load_dotenv
import openai
import tiktoken
# load the API key from the .env file
load_dotenv()
# set the API key for the openai library
openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_EUS_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AOAI_EUS_API_KEY")

system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 250 # limiting the response to 250 tokens, can be adjusted based on the use case.
# hard limit here for GPT3.5 Turbo
token_limit= 500
conversation=[]
conversation.append(system_message)
user_input = ''

def gpt4_completion(engine='gpt-35-turbo-version0301-eus', message = conversation, max_tokens=max_response_tokens):
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=message)
    return response['choices'][0]['message']['content']

user_input = input("User: ")      
conversation.append({"role": "user", "content": user_input})
response = gpt4_completion(message = conversation)
print(response)