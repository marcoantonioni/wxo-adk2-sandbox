#greetings.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(name="MA42021_greeting")
def greeting() -> str:
    """
    Greeting for everyone   
    """

    greeting = "Hello World"
    return greeting
