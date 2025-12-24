# Memos

```bash

git config user.name "marcoantonioni"
git config user.email "antonioni.marco@gmail.com"

git add .
git commit -m "update"
git push -u origin main
```

## commands memos

```bash

orchestrate env list

orchestrate env activate local

orchestrate models list

orchestrate agents list

orchestrate tools list

orchestrate connections list

orchestrate server logs --name dev-edition-wxo-server-1
orchestrate server logs | grep dev-edition-wxo-server-1

orchestrate server logs | grep dev-edition-wxo-server-worker-1

# container names
docker inspect --format '{{.Name}}' $(docker ps -q) | sed 's/\///g'

```

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

