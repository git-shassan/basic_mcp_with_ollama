=== Setup fastmcp: 



=== To inspect MCP:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"
# Download and install Node.js:
nvm install 25
```
```
npm install -g @modelcontextprotocol/inspector
```
```
mcp-inspector /home/farrukh/MCP/mcp/bin/python /home/farrukh/MCP/websearch.py
```
Then use "connect" to connect to the MCP server



