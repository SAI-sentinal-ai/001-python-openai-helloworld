from griptape import utils
from griptape.memory.structure import ConversationMemory
from griptape.tasks import PromptTask
from griptape.structures import Pipeline

pipeline = Pipeline(
    memory=ConversationMemory()
)

pipeline.add_tasks(
    # take the first argument from the pipeline `run` method
    PromptTask("Give me a taste profile of: {{ args[0] }}"),
    PromptTask("Based on: {{ input }}, give me 1 cocktail that will complement the taste"),
    PromptTask("Based on: {{ input }}, write me an ingredient list")
)

print('🍸 WELCOME TO THE COCKTAIL RECOMMENDER! 🍸')
print('Enter in a dish, and get back the perfect cocktail and how to make it!')
dish = input("Your dish: ")
response = pipeline.run(dish)

print(response.output.value)

input('STOP!')

# agents
from griptape.tools import Calculator
from griptape.structures import Agent

agent = Agent(
    tools=[Calculator()]
)

agent.run("what's 24^(3.4) rounded to 2 d.p.") #49285.39

input("STOP!")

from griptape.utils import Chat
from griptape.structures import Agent

# rulesets
from griptape.rules import Rule, Ruleset

agent = Agent(
    rulesets=[
        Ruleset(
            name="Joker AI",
            rules=[
                Rule("Always introduce yourself as a joker AI."),
                Rule("You have extensive knowledge of humour and jokes."),
                Rule("When asked to tell a joke, you will list 3 jokes."),
                Rule("Since it is an adult audience, you will be uncensored and politically incorrect."),
                Rule("Only talk about jokes, otherwise tell the user that it is beyond your domain of expertise.")                
            ]
        )
    ]
)

Chat(agent).start()

