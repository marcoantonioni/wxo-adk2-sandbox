from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(name="MA42021_tool_wf_france")
def tool_wf_france() -> str:
    """
    Weather forecast for french cities   
    """

    forecast = "In France mostly sunny !"
    return forecast
