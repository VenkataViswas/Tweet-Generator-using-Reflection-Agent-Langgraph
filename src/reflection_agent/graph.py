from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import add_messages
from reflection_agent.chains import generation_chain,reflection_chain
from langgraph.graph import StateGraph,END
class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

REFLECT ="reflect"
GENERATE = "generate"


def generate_node(state:MessageState):
    return {"messages":[generation_chain.invoke(
        {
            "messages":state["messages"]
        }
    )]}

def reflection_node(state: MessageState):
    tweet = state["messages"][-1].content

    res = reflection_chain.invoke({
        "messages": [HumanMessage(content=tweet)]
    })

    return {"messages": [HumanMessage(content=res.content)]}

def should_continue(state:MessageState):
    if len(state["messages"])>6:
        return END 
    return REFLECT


builder = StateGraph(state_schema=MessageState)
builder.add_node(GENERATE,generate_node)
builder.set_entry_point(GENERATE)

builder.add_node(REFLECT,reflection_node)
builder.add_conditional_edges(GENERATE,should_continue,path_map={
    END:END,
    REFLECT:REFLECT
})

builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
if __name__=="__main__": 
    # for drawing to cmd 
    # graph.get_graph().draw_mermaid())
    graph.get_graph().draw_mermaid_png(output_file_path="flow.png")
    