# python -m pip install 'langchain[llms]'
# echo "export OPENAI_API_KEY=<your_key> >> ~/.zshrc"
# source ~/.zshrc

#----- hello world

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage
)
import os

chat = ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0.9)

messages = []

k = 0
while k < 1: 
    message = input("---- User:\n")
    usr_msg = HumanMessage(content=message)
    messages.append(usr_msg)
    ai_msg = chat(messages)
    print("---- GPT:")
    print(ai_msg.content)
    messages.append(ai_msg)
    k = k + 1

input('Continue? ')
#----- prompt templates

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["product","entity"],
    template="What is a catchy name for a {entity} that makes {product}?",
)

#p = prompt.format(product="cheese",entity="Italian farm")
p = prompt.format(product="electric razors",entity="German factory")

print('Prompt: ',p)

from langchain.chains import LLMChain, SimpleSequentialChain

messages = []
usr_msg = HumanMessage(content=p)
messages.append(usr_msg)
completion = chat(messages)
print(completion.content)

input('Continue? ')

#----- chains
# Chain 1: 
prompt1 = PromptTemplate(
    input_variables=["dish"],
    template="What is the taste profile for {dish}? ONLY REPORT THE TASTE PROFILE, NO BOILER PLATE OR QUALIFICATIONS SUCH AS 'AS AN AI MODEL'.",
)
chain1 = LLMChain(llm=chat, prompt=prompt1)

# Chain 2: 
prompt2 = PromptTemplate(
    input_variables=["tasteprofile"],
    template="What is 1 cocktail, 1 mocktail, and 1 juice that will be perfect to pair with {tasteprofile}? NO BOILER PLATE OR QUALIFICATIONS SUCH AS 'AS AN AI MODEL'.",
)
chain2 = LLMChain(llm=chat, prompt=prompt2)

# Chain 3: 
prompt3 = PromptTemplate(
    input_variables=["drinks"],
    template="Create an ingredient list for the cocktails and drinks: {drinks}? NO BOILER PLATE OR QUALIFICATIONS SUCH AS 'AS AN AI MODEL'.",
)
chain3 = LLMChain(llm=chat, prompt=prompt3)

# Combine the chains
full_chain = SimpleSequentialChain(chains=[chain1, chain2, chain3], verbose=True)

# Run the chain specifying the input variable for the first chain.
#result = full_chain.run("Melted cheese between bread, served with tomato soup.")
#result = full_chain.run("A medium-rare beef steak, served with thick cut fries and tomato relish.")
result = full_chain.run("Doritos.")
print(result)
