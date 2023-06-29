# %%
import openai
import json
import os
import subprocess

# load and set our key
openai.api_key = os.environ["OPENAI_API_KEY"]

# %%
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's 24.546+33.2323?"}],
)

# %%
reply_content = completion.choices[0].message.content
print(reply_content)

# %%
def add_two_numbers(number1, number2):
    """Takes two numbers as input and returns the sum of these numbers."""
    return number1 + number2

# %%
def bible_verse(letter_number,chapter, verse):
    """Takes two chapter and verse input and returns the scripture in JSON."""
    if letter_number:
        x = f"https://bible-api.com/{letter_number}%20{chapter}%20{verse}"
    else:
        x = f"https://bible-api.com/{chapter}%20{verse}"
    return x

# %%
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "Moonlanding."}],
    functions=[
    {
    "name": "add_two_numbers",
    "description": "Takes two numbers as input and returns the sum of these numbers.",
    "parameters": {
        "type": "object",
        "properties": {
            "number1": {
                "type": "number",
                "description": "The first number to add."
            },
            "number2": {
                "type": "number",
                "description": "The second number to add."
            }
        },
        "required": ["number1", "number2"]
    }
    },
    {
    "name": "bible_verse",
    "description": "Returns a bible verse.",
    "parameters": {
        "type": "object",
        "properties": {
            "letter_number": {
                "type": "string",
                "description": "The number of letter , e.g., 1 for 1 Corinthians."
            },
            "book_name": {
                "type": "string",
                "description": "The name of Bible book, e.g., John, Luke, Numbers."
            },
            "verse": {
                "type": "string",
                "description": "The chapter and verse, e.g., 3:16."
            }
        },
        "required": ["letter_number","book_name", "verse"]
    }
    },
    {
    "name": "event_details",
    "description": "Returns details of an event.",
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "A description of the event in 1 sentence"
            },
            "city": {
                "type": "string",
                "description": "The city where the event took place"
            },
            "date": {
                "type": "string",
                "description": "Month and year of the event"
            }
        },
        "required": ["description","city", "date"]
    }
    }  
],
#function_call={"name": "add_two_numbers"},
function_call="auto",
)

# %%
reply_content = completion.choices[0]
reply_content

# %%
reply_content = completion.choices[0].message

funcs = reply_content.to_dict()['function_call']['arguments']
funcs = json.loads(funcs)
print(funcs)
#print(add_two_numbers(funcs['number1'],funcs['number2']))
#url = bible_verse(funcs['letter_number'],funcs['book_name'],funcs['verse'])
#import requests
#response = requests.get(url)
#data = json.loads(response.text)
#print(data['text'])

# %%
from pydantic import BaseModel, Field
from simpleaichat import AIChat

ai = AIChat(
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model="gpt-3.5-turbo-0613",
    params={"temperature": 0.0},
)

class get_event_metadata(BaseModel):
    """Based on an event, fill out the details"""

    description: str = Field(description="Description of event")
    city: str = Field(description="City where event occured")
    year: int = Field(description="Year when event occured")
    month: str = Field(description="Month when event occured")

# returns a dict, with keys ordered as in the schema
ai("First iPhone announcement", output_schema=get_event_metadata)


