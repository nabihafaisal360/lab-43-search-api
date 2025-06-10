from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

from GCS_agent.configuration import llm_with_tools
#from agent.tools import tools
from GCS_agent.tools import search_tool
from GCS_agent.state import AgentState

import json

# State definition is now imported from react_agent.state
# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], ...]  # We'll set reducer below

# from langgraph.graph.message import add_messages
# AgentState.__annotations__["messages"] = Annotated[Sequence[BaseMessage], add_messages]

# tool lookup
tools_by_name = {search_tool.name: search_tool}

# Tool node
def tool_node(state: AgentState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Check if the tool is google_search and adjust arguments
        if tool_name == search_tool.name and "__arg1" in tool_args:
            tool_args = {"query": tool_args["__arg1"]}

        tool_result = tools_by_name[tool_name].invoke(tool_args)
        
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}

# llm_with_tools node
def call_llm_with_tools(state: AgentState, config: RunnableConfig):
    system_prompt = SystemMessage(
        "You are a helpful AI assistant, please respond to the users query to the best of your ability! and remember key details"
    )
    response = llm_with_tools.invoke([system_prompt] + state["messages"], config)
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not getattr(last_message, "tool_calls", None):
        return "end"
    else:
        return "continue"

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_llm_with_tools)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)
workflow.add_edge("tools", "agent")
graph = workflow.compile()