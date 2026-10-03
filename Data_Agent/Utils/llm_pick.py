from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


def pick_llm(level: str):
    """
    Picks the appropriate LLM based on the level of the question.

    Args:
        level (str): The level of the question, can be "low", "medium", or "high".

    Returns:
        ChatOpenAI: The LLM instance to be used.
    """
    # if level.lower() == "low":
    #     llm = ChatOpenAI(model_name="gpt-5.6-luna", temperature=0)
    # elif level.lower() == "medium":
    #     llm = ChatOpenAI(model_name="gpt-5.6-terra", temperature=0)
    # elif level.lower() == "high":
    #     llm = ChatOpenAI(model_name="gpt-5.6-sol", temperature=0)
   
    # else:
    #     raise ValueError(f"Unsupported level: {level}")

    # return llm

    # model kwargs
def pick_llm(level: str):
    if level.lower() == "low":
        llm = ChatGroq(model="openai/gpt-oss-safeguard-20b", temperature=0)
    elif level.lower() == "medium":
        llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    elif level.lower() == "high":
        llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    # elif level.lower() == "claude":
    #     llm = ChatAnthropic(model_name="claude-sonnet-5")
    else:
        raise ValueError(f"Unsupported level: {level}")
    return llm