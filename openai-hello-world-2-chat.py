import os
import openai
import time

openai.api_key = os.environ["OPENAI_API_KEY"]

responses = []
#system_msg = input("GPT: What type of chatbot would you like to create? ")
system_msg = 'Sassy, sarcastic assistant using emojis and rhymes.'
responses.append({"role": "system", "content": system_msg})

print("---- GPT:\nSay hello to your new assistant!")
while input != "quit()": 
    response = input("---- User:\n")
    responses.append({"role": "user", "content": response})
    print('---- GPT:')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=responses)
    reply = response["choices"][0]["message"]["content"]
    responses.append({"role": "assistant", "content": reply})
    print(reply)