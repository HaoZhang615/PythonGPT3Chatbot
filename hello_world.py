import openai
from dotenv import load_dotenv
import os

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['<<END>>']):
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
    prompt = 'You are a nurse and I am your patient. I: I am not feeling well today, I would like some medicien.'
    response = gpt3_completion(prompt)
    print(response)