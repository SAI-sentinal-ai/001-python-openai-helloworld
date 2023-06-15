# get SERPAPI key @ https://serpapi.com/
# echo "export SERPAPI_API_KEY=<your_key> >> ~/.zshrc"
# echo "export OPENAI_API_KEY=<your_key> >> ~/.zshrc"
# pip install google-search-results

#----- tools

import re
import matplotlib.pyplot as plt
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

# First, let's load the language model we're going to use to control the agent.
llm = ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
# list of tools https://python.langchain.com/en/latest/modules/agents/tools/getting_started.html
tools = load_tools(["serpapi", "llm-math", "terminal","open-meteo-api"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# why do we need this?! see: https://github.com/hwchase17/langchain/issues/1358#issuecomment-1520834694

try:
    response = agent.run("What is simpleaichat github repo about?")
    #response = agent.run("List all files in my current directory?")
    #response = agent.run("Who is Epictetus?")
    #response = agent.run("What is the weather in Auckland, NZ today?")
    a = 1
except Exception as e:
    response = str(e)
    if "Could not parse LLM output: `" not in response:
        raise e

    match = re.search(r"`(.*?)`", response)

    if match:
        last_output = match.group(1)
        print("Last output:", last_output)
    else:
        print("No match found")

input('Continue?')

#----- create own tools
from langchain.agents import Tool
import pandas as pd
import subprocess

def load_csv_file(f_name):
    df = pd.read_csv(f_name)
    return df

csv_tool = Tool(
    name='CSV file reader',
    func=load_csv_file,
    description="Useful for when you need to read a CSV file for data analysis."
)

def yt_search(topic):
    cmd = f'yt-dlp ytsearch5:{topic} --get-title'
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
    vidlist = output.strip().split('\n')
    titles = [title for title in vidlist if "WARNING" not in title and "n =" not in title]
    return titles

utube_tool = Tool(
    name='Youtube search',
    func=yt_search,
    description="Useful for when you need to search YoTube."
)

#serpapi_tool = load_tools(["serpapi"])

from langchain.chains.conversation.memory import ConversationBufferWindowMemory

tools_b = [csv_tool,utube_tool]
#tools_b = [csv_tool]

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=3,
    return_messages=True
)

# create our agent
conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools_b,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory
)

conversational_agent("Find youtube videos on the topic 'reddit' and based on these, (1) tell me the overall sentiment of the videos and (2) recommend a youtube video that I should create that will get the most views, and give me a SEO based title for this video.")


fixed_prompt = '''Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.'''

conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt



#----- other tools

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests
from PIL import Image
from langchain.tools import BaseTool

hf_model = "Salesforce/blip-image-captioning-large"
device = 'cuda' if torch.cuda.is_available() else 'cpu'
processor = BlipProcessor.from_pretrained(hf_model)
model = BlipForConditionalGeneration.from_pretrained(hf_model).to(device)

def image_caption_tool(input="img_url"):
    # download the image and convert to PIL object
    image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
    # preprocess the image
    inputs = processor(image, return_tensors="pt").to(device)
    # generate the caption
    out = model.generate(**inputs, max_new_tokens=40)
    # get the caption
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

img_cap_tool = Tool(
    name='Image captioner',
    func=image_caption_tool,
    description=("Use this tool to find what an image shows given the URL. "
    "You will return a detailed caption describing the image, including colour palette.")
)    

# replace the tools
tools_c = [img_cap_tool]

# create our agent
conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools_c,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory
)

img_url = 'https://images.unsplash.com/photo-1543349689-9a4d426bee8e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1401&q=80' 

conversational_agent(f"What does this image show?\n{img_url}")

