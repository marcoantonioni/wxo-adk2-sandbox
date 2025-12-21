# Agents

```bash
export _WXO_SANDBOX=/home/marco/wxo/wxo-adk2-sandbox
```

## greeter

```bash
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/greetings.py
orchestrate agents import -f ${_WXO_SANDBOX}/agents/greeter.yaml
```

```bash
orchestrate agents remove --name MA42021_greeter --kind native
orchestrate tools remove --name MA42021_greeting
```

## customer_care_agent


```bash
orchestrate connections add -a MA42021_service-now
orchestrate connections configure -a MA42021_service-now --env draft --type team --kind basic --url https://dev292696.service-now.com
orchestrate connections set-credentials -a MA42021_service-now --env draft -u admin -p '...'

orchestrate connections configure -a MA42021_service-now --env live --type team --kind basic --url https://dev292696.service-now.com
orchestrate connections set-credentials -a MA42021_service-now --env live -u admin -p '...'

orchestrate connections list
```

```bash
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/customer_care/get_my_claims.py
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/customer_care/get_healthcare_benefits.py
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/customer_care/search_healthcare_providers.py

orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/servicenow/create_service_now_incident.py -r ${_WXO_SANDBOX}/tools/servicenow/requirements.txt -a MA42021_service-now
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/servicenow/get_my_service_now_incidents.py -r ${_WXO_SANDBOX}/tools/servicenow/requirements.txt -a MA42021_service-now
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/servicenow/get_service_now_incident_by_number.py -r ${_WXO_SANDBOX}/tools/servicenow/requirements.txt -a MA42021_service-now

orchestrate agents import -f ${_WXO_SANDBOX}/agents//service_now_agent.yaml
orchestrate agents import -f ${_WXO_SANDBOX}/agents/customer_care_agent.yaml

orchestrate tools list
orchestrate agents list

```

<pre>
Test: 
Show my benefits related to mental health
</pre>

```bash
orchestrate agents remove --name MA42021_customer_care_agent --kind native
orchestrate tools remove --name MA42021_get_healthcare_benefits
orchestrate tools remove --name MA42021_get_my_claims
orchestrate tools remove --name MA42021_search_healthcare_providers

orchestrate agents remove --name MA42021_service_now_agent --kind native
orchestrate tools remove --name MA42021_create_service_now_incident
orchestrate tools remove --name MA42021_get_my_service_now_incidents
orchestrate tools remove --name MA42021_get_service_now_incident_by_number

orchestrate connections remove --app-id MA42021_service-now
```

## healthcare_agent

```bash
orchestrate tools import -k openapi -f ${_WXO_SANDBOX}/tools/openapi/get_healthcare_providers.yaml
orchestrate agents import -f ${_WXO_SANDBOX}/agents/healthcare_agent.yaml
```

```bash
orchestrate agents remove --name MA42021_healthcare_agent --kind native
orchestrate tools remove --name MA42021_getHealthCareProviders
```

## langflow_agent
```bash
orchestrate tools import -k langflow -f ${_WXO_SANDBOX}/tools/langflow/transcripts_action_item_extractor.json
orchestrate agents import -f ${_WXO_SANDBOX}/agents/langflow_agent.yaml
```

Test
<pre>
**[09:00:15] Sarah:** Okay everyone, let's officially kick off. The core Q3 review is actually solid. . Honestly, very good. We just have these, like, these weird loose ends.
**[09:01:22] Alice:** Uh, yeah. On the comms part, I was just thinking about that Q3 deck. So, uh, I'm taking the lead on the client update. We're good there. Alice to send the Q3 deck by Friday. I mean, that's what I said before, but yeah, it's firm.
**[09:02:40] Mark:** Yeah, and I know Bob, you're slammed, but what's the ETA on the new API documentation? That's kinda our bottleneck now.
**[09:03:01] Bob:** Uh-huh. Bob will review the API docs tomorrow. Yeah, that's completely locked in. I just need a clean four hours for the final check. Oh, and John, are you on the call?
**[09:03:55] John:** (unintelligible) Yeah, I'm here. Customer call. Yes. John: I'm speaking with the customer by 10/12. We can move that out of the blocker list.
**[09:04:30] Sarah:** Fantastic, okay. So John's clear. Now, the public announcement, let's not let that slip. We need to get the statement ready. Draft the announcement before Oct 15 so Legal has, like, you know, a full week.
**[09:05:15] Mark:** And one other thing, admin stuff, but critical. Site visits are coming up fast. We should also book rooms next week for the new candidates. I'll flag that in a separate chat right after this.
**[09:06:05] Sarah:** Sounds like a plan. Thanks for the clarity on those dates. Let's sync up again. Bye.
**[09:06:12] Marco:** Great I'll send you a note.
</pre>

```bash
orchestrate agents remove --name MA42021_langflow_agent --kind native
orchestrate tools remove --name MA42021_transcripts_action_item_extractor
```

## web_chat_customization

```bash
orchestrate agents import -f ${_WXO_SANDBOX}/agents/web_chat_configuration.yaml
```

```bash
orchestrate agents remove --name MA42021_web_chat_configuration --kind native
```

## agent_style_default

```bash
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/tool_document.py
orchestrate agents import -f ${_WXO_SANDBOX}/agents/agent_style_default.yaml
```

```bash
orchestrate agents remove --name MA42021_agent_style_default --kind native
orchestrate tools remove --name MA42021_tool_document
```

## agent_style_react

```bash
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/user_activities.py
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/user_data.py
orchestrate agents import -f ${_WXO_SANDBOX}/agents/agent_style_react.yaml
```

Test
<pre>
Check the current status and activities of user marco.
</pre>

```bash
orchestrate agents remove --name agent_style_react --kind native
orchestrate tools remove --name MA42021_user_data
orchestrate tools remove --name MA42021_user_activities
```

## agent_style_planner

```bash
#orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/tool_scheduler.py
#orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/tool_executor.py
orchestrate tools import -k python -f ${_WXO_SANDBOX}/tools/tool_planner.py
orchestrate agents import -f ${_WXO_SANDBOX}/agents/agent_style_planner.yaml
```

Test
<pre>
Get plan alpha with budget of 1300$ and a rollout window of 30 weeks.

Get plan alpha with budget of 1150$ and a rollout window of 40 weeks.

Get plan beta with budget of 3100$ and a rollout window of 53 weeks.

Get plan beta with budget of 3500$ and a rollout window of 33 weeks.

</pre>

```bash
orchestrate agents remove --name MA42021_agent_style_planner --kind native
orchestrate tools remove --name MA42021_tool_planner
```

