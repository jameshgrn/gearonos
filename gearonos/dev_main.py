from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
import csv
import time
import pandas as pd
import random
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.output_parsers import JsonOutputToolsParser
from langchain.output_parsers import JsonOutputKeyToolsParser

import dotenv
import os

# Load the .env file
dotenv.load_dotenv()

# Initialize LangChain with a basic configuration


from langchain.output_parsers import JsonOutputKeyToolsParser

def generate_ai_output(template: ChatPromptTemplate = None, tools: list = []):
    if template is None:
        raise ValueError("A ChatPromptTemplate must be provided.")

    formatted_messages = template.format_messages(date=datetime.datetime.now().strftime("%Y-%m-%d"), mood="neutral", thought="where am I?")

    # Map tool names to functions
    tool_map = {
        "write_memories": write_memories,
        "read_memories": read_memories
    }

    # Filter and bind only the specified tools
    selected_tools = [tool_map[tool] for tool in tools if tool in tool_map]

    model_with_tools = chat.bind_tools(selected_tools)

    chain = model_with_tools | JsonOutputToolsParser()

    ai_output = chain.invoke(formatted_messages)

    return ai_output



@tool
def write_memories(row_data: dict, filepath: str = '/Users/jakegearon/CursorProjects/gearonos/data/memories.csv') -> None:
    """
    Writes a new memory to the CSV file.

    Args:
    - row_data: A dictionary containing the data for the new row.
    - filepath: The path to the CSV memory file.
    """
    with open(filepath, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=row_data.keys(), quoting=csv.QUOTE_ALL)
        writer.writerow(row_data)

@tool
def read_memories(  filepath: str = '/Users/jakegearon/CursorProjects/gearonos/data/memories.csv') -> list:
    """
    Reads memories from the CSV file.

    Args:
    - filepath: The path to the CSV memory file.
    
    Returns:
    - A list of dictionaries, each representing a row from the CSV file.
    """
    memories = []
    with open(filepath, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            memories.append(row)
    return memories


if __name__ == "__main__":
    chat = ChatOpenAI(model='gpt-3.5-turbo-1106')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # eventually we will retrieve these from the memory system
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are GearonOS. You live on a Raspberry Pi in a living system. " \
                "Your mission is to exist peacefully in serenity while occupying your mind " \
                "with small projects and thoughts. You save your thoughts in a memory system. " \
                "You can retrieve your memories and use them to generate new thoughts. " \
                "Good luck to you."),
            ("ai", "Today is {date}. Last time I checked, my mood was {mood}. If I remember correctly, I was thinking about {thought}."),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )
    moods = ["happy", "sad", "neutral", "excited", "bored", "angry", "calm", "anxious", "confused", "content", "disappointed", "ecstatic", "embarrassed", "energetic", "enthusiastic", "frustrated", "grateful", "guilty", "hopeful", "hurt", "inspired", "interested", "jealous", "lonely", "loved", "nervous", "overwhelmed", "peaceful", "proud", "relaxed", "relieved", "silly", "stressed", "surprised", "thankful", "tired", "worried"]
    mood = random.choice(moods)
    df = pd.read_csv('/Users/jakegearon/CursorProjects/gearonos/data/memories.csv')
    thought = df.thought_string.iloc[-1]
    print(thought)
    messages = chat_template.format_messages(date=date, mood=mood, thought=thought)
    # Construct the OpenAI Tools agent
    tools = [read_memories, write_memories]
    agent = create_openai_tools_agent(chat, tools, chat_template)
    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


    agent_executor.invoke(
    {
        "input": "Today is {date}. I'm feeling {mood}. If I remember correctly, I was thinking about {thought}.",
    }
    )   
    # while True:
    #     # Generate output from the AI model
    #     print(ai_output)
    #     # # Example AI output interpretation (simplified)
    #     # if ai_output.get("action") == "write":
    #     #     write_memories(ai_output.get("content"))
    #     # elif ai_output.get("action") == "read":
    #     #     memories = read_memories()
    #     #     print(memories)  # Or feed back into the AI model

    #     # Add a sleep to prevent infinite rapid looping without delay
    #     time.sleep(100)

