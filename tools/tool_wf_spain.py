from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(name="MA42021_tool_wf_spain")
def tool_wf_spain() -> str:
    """
    Weather forecast for spanish cities   
    """

    forecast = "In Spain wida loca !"
    return forecast
