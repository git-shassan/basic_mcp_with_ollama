# New style of code... 
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import asyncio
from langchain_core.messages import convert_to_messages

client = MultiServerMCPClient(  
    {
        "math": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": ["/home/syed/experiments/AI/aisquad/new/server.py"],
        },
        "kubernetes": {
            "transport": "stdio",
            "command": "npx",
            "args": [
              "-y",
              "kubernetes-mcp-server@latest"
              ],
        }
    }
)
model = init_chat_model( model="granite3.3:8b", model_provider="ollama", base_url="http://192.168.22.4:11434") 

async def get_tools():
	tools = await client.get_tools()
	return(tools)

my_tools = asyncio.run(get_tools())
for tool in my_tools:
	print(f"Tool Name: {tool.name}")
	print(f"Description: {tool.description}")
	print("-" * 20)

agent = create_agent(
    model,
    my_tools,
    )


async def get_response(agent):
    response = await agent.ainvoke(
        {"messages": [{"role": "system", "content": "you are helpful model who can use tools to get information about openshift cluster"}, {"role": "user", "content": "List all the namespaces in the current cluster and the number of pods running in each one of them. Don't tell me the commands for it, but run those commands yourself and tell me the final answer in a table"}]}
        )
    return(response)
        # {"messages": [{"role": "system", "content": "you are helpful model who can use tools to get information about openshift cluster"}, {"role": "user", "content": "can you use your availble tools to tell me how many nodes are there in my openshift cluster? Don't tell me the commands for it, but run those commands yourself and tell me the final answer"}]}
    return(response)

response = asyncio.run(get_response(agent))

print("============================== web ===")
print(response)
print("----------------")
for message in convert_to_messages(response["messages"]):
    message.pretty_print()
