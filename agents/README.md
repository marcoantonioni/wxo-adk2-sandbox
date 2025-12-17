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
orchestrate connections set-credentials -a MA42021_service-now --env draft -u admin -p 'Gp=$H4XQxh5l'

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
