from langchain.memory.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain.tools.google_places.tool import GooglePlacesTool
# from langchain.schema.messages import HumanMessage, AIMessage
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain

import streamlit as st
import pandas as pd


@st.cache_data
def load_data(filename) -> pd.DataFrame:
    df = pd.read_csv(f"data/{filename}")
    return df


# @st.cache_resource
def create_pandas_dataframe_agent(
        llm,
        df: pd.DataFrame,
        prefix: str,
        suffix: str,
        # format_instructions: str,
        verbose: bool,
        **kwargs) -> AgentExecutor:
    """Construct a pandas agent from an LLM and dataframe."""

    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected pandas object, got {type(df)}")

    input_variables = ["df", "input", "chat_history", "agent_scratchpad"]

    # Set up memory
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    memory = ConversationBufferMemory(chat_memory=msgs, memory_key="chat_history")

    tools = [PythonAstREPLTool(locals={"df": df}), GooglePlacesTool()]

    prompt = ZeroShotAgent.create_prompt(
        tools=tools,
        prefix=prefix,
        suffix=suffix,
        # format_instructions=format_instructions,
        input_variables=input_variables
    )
    partial_prompt = prompt.partial(df=str(df.head()))

    llm_chain = LLMChain(
        llm=llm,
        prompt=partial_prompt
    )
    tool_names = [tool.name for tool in tools]

    agent = ZeroShotAgent(llm_chain=llm_chain,
                          allowed_tools=tool_names, verbose=verbose)

    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=verbose,
        memory=memory,
        **kwargs
    )
