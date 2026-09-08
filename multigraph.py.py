from langgraph.graph import StateGraph, MessagesState, START, END

def core_processing_node(state: MessagesState):
    # Your graph logic goes here
    return {"messages": [{"role": "assistant", "content": "Processed by sub-graph!"}]}

# Build and compile the sub-graph
sub_graph_builder = StateGraph(MessagesState)
sub_graph_builder.add_node("process", core_processing_node)
sub_graph_builder.add_edge(START, "process")
sub_graph_builder.add_edge("process", END)

compiled_sub_graph = sub_graph_builder.compile()


from langchain_core.tools import tool

@tool
def trigger_sub_workflow(user_query: str) -> str:
    """Use this tool when you need specialized, multi-step sub-processing 
    for complex queries or data analytics workflows.
    """
    # Invoke the graph using the input provided by the parent agent
    response = compiled_sub_graph.invoke({"messages": [("user", user_query)]})
    
    # Extract and return the final state or last message string
    return response["messages"][-1].content


from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Initialize the primary model
llm = ChatOpenAI(model="gpt-4o")

# Group all available tools
tools = [trigger_sub_workflow]

# Create the master agent
parent_agent = create_react_agent(llm, tools=tools)


final_output = parent_agent.invoke(
    {"messages": [("user", "Run the complex analytics workflow for my query.")]}
)
print(final_output["messages"][-1].content)



parent -> messagestate -> child -> response -> parent