# wxo-adk2-sandbox
wxo adk v2 samples

## commands memos

### FastMCP
```bash
pip install mcp
pip show mcp
```

### MCP Inspector
```bash
npx @modelcontextprotocol/inspector@latest
```

### Formatter, Linter
```bash
pip install black
pip install pylint
```

### Black formatter via command line
```bash
export PYTHONPATH=~/.vscode/extensions/ms-python.black-formatter-2025.2.0/bundled/libs
python -m black .
```

## other

### ServiceNow developer account

https://developer.servicenow.com/dev.do

```bash
orchestrate connections add -a MA42021_service-now
orchestrate connections configure -a MA42021_service-now --env draft --type team --kind basic --url https://dev292696.service-now.com
orchestrate connections set-credentials -a MA42021_service-now --env draft -u admin -p '....'
```


https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/20250501-1821-5146-80d6-0ef0535f5342