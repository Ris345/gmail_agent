from agno.agent import Agent
from agno.models.openai import OpenAIChat
import os.path
import logging
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize the agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are spam cleaning bot, you will periodically check for spam emails and delete them.",
    tools=[],
    show_tool_calls=True,
    markdown=True
)
# agent.print_response("Provide instructions on what I need to tweak with spam cleaner bot.", stream=True)

# agent work flow 

def check_mail():
    """ agent is going to check your email periodically 2 days it is 
    going to check both inbox and spam if the agent finds spam related data agent performs the deletetion function autonoously"""
    print('checking email')


def remove_junk():
    """After identifying the junk agent will perform a deletion action to remove all the junk email"""
    print('deleting junk')