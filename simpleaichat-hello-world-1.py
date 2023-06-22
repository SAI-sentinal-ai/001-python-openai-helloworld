# python -m pip install simpleaichat

from simpleaichat import AIChat
import os
import time

api_key=os.environ["OPENAI_API_KEY"]

#AIChat()

#input("STOP!")

#AIChat("Seneca","Behave as the ancient stoic philosopher. Speak as Seneca would.")

import platform
from simpleaichat.utils import wikipedia_search, wikipedia_search_lookup
from run_cmd import execute_local_bash
from rich.console import Console

# This uses the Wikipedia Search API.
# Results from it are nondeterministic, your mileage will vary.
def search(query):
    """Search the internet."""
    wiki_matches = wikipedia_search(query, n=3)
    return {"context": ", ".join(wiki_matches), "titles": wiki_matches}

def lookup(query):
    """Lookup more information about a topic."""
    page = wikipedia_search_lookup(query, sentences=3)
    return page

def bashcmd(query):
    """Execute bash commands locally."""
    cmd = ai(f"Give a command to do: {query} on {platform.system()}. Only return the command, without quotes or any other text.")
    print(cmd) # for debugging purposes
    output = execute_local_bash(cmd)
    return output

params = {"temperature": 0.0, "max_tokens": 300}
ai = AIChat(params=params, console=False)

response = ai("List files in my current directory!", tools=[bashcmd])
print(response['context'])

input("STOP!")
