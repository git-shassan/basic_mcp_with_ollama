= Setup fastmcp: 

```
pip install langchain_community
pip install fastmcp
pip install ddgs
```
```
python --version
Python 3.12.9
pip --version
pip 23.2.1 <<snip>>
```

=== Create server and client apps:
See other files

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

=== Install mcp-server & configure:
export GITHUB_TOKEN first

```
provider-url: "http://192.168.22.4:11434"
model: "ollama:llama3.2:3b"

mcpServers:
   filesystem-builtin:
     type: "builtin"
     name: "fs"
     options:
       allowed_directories: ["/root"]
       allowedTools: ["read_file", "write_file", "list_directory"]
   github:
     type: local
     command: ["podman", "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN=${env://GITHUB_TOKEN}", "ghcr.io/github/github-mcp-server"]
     environment:
       DEBUG: "${env://DEBUG:-false}"
       LOG_LEVEL: "${env://LOG_LEVEL:-info}"
   mytool:
     type: "local"
     command: "/home/farrukh/MCP/mcp/bin/python"
     args: "/home/farrukh/MCP/websearch.py"

```
Then run the MCP user




