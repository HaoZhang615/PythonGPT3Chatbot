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
# Examples here:
# conversation = {"role": "system", "content": "Assistant is an intelligent chatbot designed to help users answer technical questions about Azure OpenAI Serivce. Only answer questions using the context below and if you're not sure of an answer, you can say 'I don't know'.

# Context:
# - Azure OpenAI Service provides REST API access to OpenAI's powerful language models including the GPT-3, Codex and Embeddings model series.
# - Azure OpenAI Service gives customers advanced language AI with OpenAI GPT-3, Codex, and DALL-E models with the security and enterprise promise of Azure. Azure OpenAI co-develops the APIs with OpenAI, ensuring compatibility and a smooth transition from one to the other.
# - At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes requiring applicants to show well-defined use cases, incorporating Microsoft’s principles for responsible AI use."
#}

system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 250
# hard limit here for GPT3.5 Turbo
token_limit= 4096
conversation=[]
conversation.append(system_message)

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

while(True):
    user_input = input("User: ")      
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    # if the conversation is too long, delete the oldest message
    while (conv_history_tokens+max_response_tokens >= token_limit):
        del conversation[1] 
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-version0301-eus", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = conversation,
        max_tokens=max_response_tokens
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print("\n" + response['choices'][0]['message']['content'] + "\n")