#greetings.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import datetime

@tool(name="MA42021_tool_document")
def getDocument() -> str:
    """
    Get document content
    """

    x = datetime.datetime.now()
    docContent = x.strftime("%d-%m-%Y %H:%M:%S")+"  " +"""
    title: IT services co-sourcing model
    - Official guidelines
        You must do right things.
        You cannot say lies.
    - Internal whitepapers from 2023 onwards
        withepaper1: 
            definition: it is a white definition of abstract things.
            benefits: few money.
            risks: low.
            kpi: none
            use case: cook an egg.
        withepaper2: 
            definition: it is a yellow description of things. 
            benefits: a lot of money.
            risks: very high.
            kpi: money quantity
            use case: cook a dinosaur.
    """
    return docContent
