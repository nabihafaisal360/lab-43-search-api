from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

from exa.configuration import llm_with_tools
#from agent.tools import tools
from exa.tools import search_tool
from exa.state import AgentState

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
        tool_args = tool_call["args"].copy() # Use a copy to avoid modifying the original state if not needed

        # Specifically for ExaSearchResults: ensure num_results is an int
        if tool_name == search_tool.name and "num_results" in tool_args:
            current_num_results = tool_args["num_results"]
            if isinstance(current_num_results, float):
                tool_args["num_results"] = int(current_num_results)
            elif isinstance(current_num_results, str):
                try:
                    tool_args["num_results"] = int(float(current_num_results)) # Handle "1.0" or "1"
                except ValueError:
                    # Handle cases where conversion fails, maybe log or raise
                    # For now, we'll let it pass to the tool which might error
                    pass


        tool_result = tools_by_name[tool_name].invoke(tool_args)

        # Ensure content is a string for ToolMessage
        if isinstance(tool_result, (list, dict)):
            content_str = json.dumps(tool_result)
        else:
            content_str = str(tool_result)

        outputs.append(
            ToolMessage(
                content=content_str,
                name=tool_name,
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