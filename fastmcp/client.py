import asyncio
from fastmcp import Client
client = Client("http://localhost:8000/mcp")
async def call_tool(name: str):
async def call_tool(query: str):
	async with client:
		result = await client.call_tool("mytool", {"query": query})
		print(result)
asyncio.run(call_tool("Ford"))
asyncio.run(call_tool("what did trump do today?"))
