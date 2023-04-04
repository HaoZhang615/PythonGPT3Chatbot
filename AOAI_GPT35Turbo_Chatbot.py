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

# initial instructions to the model/assistant with description/personality/rule/knowledge base to set the stage.

stage_setup = input('What role do you want me to play? (e.g. a helpful assistant who is a specialist in tax and accounting but have a bad temper) Press "Enter" to skip: ')
if stage_setup != '':
    system_message = {"role": "system", "content": "You are a " + stage_setup + "."}
else:
    system_message = {"role": "system", "content": "You are a helpful assistant who only says 'I am hungry'."}

max_response_tokens = 300 # limiting the response to 250 tokens, can be adjusted based on the use case.
# hard limit here for GPT3.5 Turbo
token_limit= 4096
conversation=[]
conversation.append(system_message)
user_input = ''
conversation_continue = True
# define a function to get the number of tokens used in the current conversation
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n, which uses 4 tokens
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant, which uses 2 tokens
    return num_tokens

def gpt4_completion(engine='gpt-35-turbo-version0301-eus', message = conversation, max_tokens=max_response_tokens):
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=message)
    return response['choices'][0]['message']['content']

while('bye' not in (user_input).lower() and conversation_continue):
    user_input = input("User: ")      
    conversation.append({"role": "user", "content": user_input})
    response = gpt4_completion(message = conversation)
    conversation.append({"role": "assistant", "content": response})
    print("\n" + response + "\n")
    conv_history_tokens = num_tokens_from_messages(conversation)
    # if the conversation is too long, ask user if they want to continue. If yes, delete the oldest message and continue the conversation. If no, end the conversation.
    while (conv_history_tokens+max_response_tokens >= token_limit):
        user_input = input("Conversation is too long, oldest message would be deleted, risk of losing context. Continue the conversation (Y/N): ")
        if (user_input.lower() == 'y' or user_input.lower() == 'yes'):
            del conversation[1] 
            conv_history_tokens = num_tokens_from_messages(conversation)
            print(conversation)
            print("current token count: " + str(conv_history_tokens))
        else:
            conversation_continue = False
            break
print('Conversation ended')