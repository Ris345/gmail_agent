from agno.agent import Agent
from agno.models.openai import OpenAIChat
import os.path
import logging
from dotenv import load_dotenv
import datetime 
from Agent.SetInterval.setinterval import setInterval
import requests 


# agent work flow 
def check_mail():
    """ agent is going to check your email periodically 2 days it is 
    going to check both inbox and spam if the agent finds spam related data agent performs the deletetion function autonoously"""

    # basically need to use the date and time methods to invoke these functions 
    # intialize a hour variable to track the time hour 
    # threshold would be 48 hrs 
    # after each hour passes the hour needs to increment the hour 
    # so basically we are creating 48 hour timer that resets everytime it completes 
    # instead of invoking the read_email func for here we will make a get req here  
    url = 'http://127.0.0.1:5000/retrieveEmails'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # If the response is JSON
        print(data)
    else:
        print(f"Error: {response.status_code}")

# this func simply invokes the func every 3 days 
setInterval(check_mail, 259200000)

def remove_junk():
    """After identifying the junk agent will perform a deletion action to remove all the junk email"""
    print('deleting junk')


# agent = Agent(
#     model=OpenAIChat(id="gpt-4o"),
#     description="How can agents invoke the function calling from tools.",
#     tools=[check_mail, remove_junk],
#     show_tool_calls=True,
#     markdown=True
# )


# agent.print_response("Look at these functions and tell me how I can make my spam cleaner successfull", stream=True)


