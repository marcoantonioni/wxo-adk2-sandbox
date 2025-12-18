#greetings.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import datetime

@tool(name="MA42021_tool_document")
def getDocument() -> str:
    """
    Get document content
    """
    x = datetime.datetime.now()

    docContent = "This is the content of document found at "+x.strftime("%d-%m-%Y %H:%M:%S")
    return docContent
