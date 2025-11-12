from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import pprint
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
        "weather": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "http://127.0.0.1:8000/mcp",
        },
        "websearch": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your websearch server on port 8001
            "url": "http://127.0.0.1:8001/mcp",
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

# model = ChatOllama(model="granite3.3:8b")
model = ChatOllama(model="llama3.2:3b")

#async def my_tools():
async def main():
    tools = await client.get_tools()  
    for tool in tools:
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print("-" * 20)
    agent = create_agent(
        model,
        tools,
    )

    ocp_response = await agent.ainvoke(
        {"messages": [{"role": "system", "content": "you are helpful model who can use tools to get information about openshift cluster"}, {"role": "user", "content": "List all the namespaces in the current cluster which start with the letter m. Don't tell me the commands for it, but run those commands yourself and tell me the final answer in a table"}]}
        # {"messages": [{"role": "system", "content": "you are helpful model who can use tools to get information about openshift cluster"}, {"role": "user", "content": "can you use your availble tools to tell me how many nodes are there in my openshift cluster? Don't tell me the commands for it, but run those commands yourself and tell me the final answer"}]}
    )
    print("============================== web ===")
    print(ocp_response)
    final_message = ocp_response["messages"][-1]
    print("----------------")
    print(final_message)
    print("----------------")
    for message in convert_to_messages(ocp_response["messages"]):
        message.pretty_print()



    # return(tools)
if __name__ == "__main__":
    asyncio.run(main())
# tools = asyncio.run(my_tools())
# 
# for tool in tools:
#     print(f"Tool Name: {tool.name}")
#     print(f"Description: {tool.description}")
#     print("-" * 20)
# 
# agent = create_agent(
#     "ollama:llama3.2:3b",
#     tools,
# )

#async def call_model():
#    math_response = await agent.ainvoke(
#        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
#    )
#    pprint(math_response)
#    weather_response = await agent.ainvoke(
#        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
#    )
#    pprint(weather_response)
#    
#asyncio.run(call_model())
