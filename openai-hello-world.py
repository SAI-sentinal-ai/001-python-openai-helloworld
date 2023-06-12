# conda create -n "openai" python=3.11 
# conda activate openai
# python -m pip install 'openai[datalib]'
# echo "export OPENAI_API_KEY=<your_key> >> ~/.zshrc"
# source ~/.zshrc
# echo $OPENAI_API_KEY

import os
import openai
 
openai.api_key = os.environ["OPENAI_API_KEY"]

# list models
models = openai.Model.list()
#print(models)

# print the first model's id
for id in models.data:
    if 'gpt' in id['root']:
        print(id['root'])

print(' ')

# create a chat completion
# options: https://platform.openai.com/docs/api-reference/chat/create#chat/create-stream
num_completions=3
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", "content": "Describe a fruit"}
        ],
    temperature=1.0,
    max_tokens=200,
    n=num_completions
)

for i in range(num_completions):
    print(chat_completion.choices[i].message.content)
