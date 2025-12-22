from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(name="MA42021_tool_wf_italy")
def tool_wf_italy() -> str:
    """
    Weather forecast for italian cities   
    """

    forecast = "In Italy sunny all days !"
    return forecast
