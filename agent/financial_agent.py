import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-70b-8192"

async def query_financial_data(prompt: str, df: pd.DataFrame) -> dict:
    try:
        llm = ChatGroq(groq_api_key = GROQ_API_KEY, model_name = MODEL_NAME, temperature = 0)

        agent = create_pandas_dataframe_agent(
            llm = llm,
            df = df,
            agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose = True,
            allow_dangerous_code = True
        )

        result = agent.invoke(prompt)
        # print(result)
        return result
    except Exception as e:
         return {"error": str(e)}