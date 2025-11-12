from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import pprint
import asyncio


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
        }
    }
)

model = ChatOllama(model="granite3.3:8b")

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
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print(math_response)
    final_message = math_response["messages"][-1]
    print(final_message)
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    print(weather_response)
    final_message = weather_response["messages"][-1]
    print(final_message)



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
