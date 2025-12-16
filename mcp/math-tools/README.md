# math-tools

## MCP Inspector
transport: STDIO

command: python

parameter: mcp/math-tools/main.py
```bash
npx @modelcontextprotocol/inspector@latest
```

## Import toolkit
```bash
orchestrate toolkits add \
  --kind mcp \
  --name math-mcp-tools \
  --description "MCP tools for Mathematical operations including calculating Factorial" \
  --package-root "./mcp/math-tools/" \
  --command '["python3", "main.py"]' \
  --tools "*"
```

orchestrate agents create --name "MathAgent" \
  --description "The agent provide precise mathematical calculations." \
  --kind native \
  --tools math-mcp-tools:factorial_digits \
  --instructions "For reasoning or English-language tasks, depend on the LLM’s own capabilities to provide answers directly. For factorial-related math queries, such as calculating the exact value or determining the number of digits, call the MCP tools to ensure precision and handle very large numbers that the LLM may struggle with. - Use tool math-mcp-tools:factorial_value to return the exact value of 𝑛! (factorial n) - Use tool math-mcp-tools:factorial_digits to return the number of decimal digits in 𝑛! (digits in factorial n)"