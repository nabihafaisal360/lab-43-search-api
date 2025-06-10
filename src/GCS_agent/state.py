# state.py
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
# Import the standard LangGraph message reducer
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Represents the state of our agent, including message history.

    Messages are managed by the 'add_messages' reducer,
    which appends new messages (lists of BaseMessage) to the existing sequence.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]