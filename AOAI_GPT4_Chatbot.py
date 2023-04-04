#Note: The openai-python library support for Azure OpenAI is in preview.
import os
from dotenv import load_dotenv
import openai
# load the API key from the .env file
load_dotenv()
# set the API key for the openai library
openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_EUS_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AOAI_EUS_API_KEY")

# prompt = "This is a test."
conversation=[{"role": "system", "content": "You are a helpful assistant."}]

def gpt4_completion(engine='gpt-35-turbo-version0301-eus', message= conversation):
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=message)
    return response

#This below line of code checks if the script is being run as the main program or being imported as a module. 
#If the script is being run as the main program, then the code block following this line will be executed. 
#Otherwise, if the script is being imported as a module, then the code block following this line will not be executed.
if __name__ == '__main__': 
    conversation = list()
    user_input = ''
    context_input = input('give a context for the following conversation, press "Enter" to skip: ')
# if there is a context, it is added to the conversation
    conversation.append(context_input)
# new line is added to the conversation
    dialog = '\n'.join(conversation)
# as long as there is no 'bye' in the user input, the conversation continues
    while ('bye' not in (user_input).lower()):
        user_input = input('User: ')
        # add user input to the conversation
        conversation.append({"role": "user", "content": user_input})
        # add new line to the conversation
        dialog = '\n'.join(conversation)
        # get completion from GPT-3 using the dialog as prompt
        completion = gpt4_completion(dialog)
        # add completion to the conversation
        conversation.append(completion)
        # add new line to the conversation for the next iteration
        dialog = '\n'.join(conversation)
        # print the completion without the 'OpenAI Assistant:' prefix
        print('OpenAI Assistant: %s' % completion)
    # print the conversation ended message
    print('Conversation ended')

while(True):
    user_input = input()      
    conversation.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-version0301-eus", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = conversation
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print("\n" + response['choices'][0]['message']['content'] + "\n")