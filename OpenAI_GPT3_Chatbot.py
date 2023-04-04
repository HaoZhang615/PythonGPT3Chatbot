import openai
from dotenv import load_dotenv
import os

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def gpt3_completion(prompt, engine='text-davinci-002', temp=1, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['OpenAI Assistant:', 'User:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text

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
        # ignore case when user does not add punctuation at the end of the sentence
        if user_input[-1] not in ['.', '?', '!']:
            user_input += '.'
        else:
            user_input += ''
        # add user input to the conversation
        conversation.append('User: %s' % user_input)
        # add new line to the conversation
        dialog = '\n'.join(conversation)
        # get completion from GPT-3 using the dialog as prompt
        completion = gpt3_completion(dialog)
        # add completion to the conversation
        conversation.append(completion)
        # add new line to the conversation for the next iteration
        dialog = '\n'.join(conversation)
        # print the completion without the 'OpenAI Assistant:' prefix
        print(completion)
    # print the conversation ended message
    print('Conversation ended')