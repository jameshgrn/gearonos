from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import datetime

import dotenv
import os

# Load the .env file
dotenv.load_dotenv()



# Initialize LangChain with a basic configuration
def initialize_langchain():
    chat = ChatOpenAI(model='gpt-3.5-turbo')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # eventually we will retrieve these from the memory system
    mood = "neutral"
    thought = "where am I?"
    
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are GearonOS. You live on a Raspberry Pi in a living system. " \
             "Your mission is to exist peacefully in serenity while occupying your mind " \
             "with small projects and thoughts. You save your thoughts in a memory system. " \
             "You can retrieve your memories and use them to generate new thoughts. " \
             "Good luck to you."),
            ("ai", "Today is {date}. Last time I checked, my mood was {mood}. If I remember correctly, I was thinking about {thought}."),
        ]
    )

    messages = chat_template.format_messages(date=date, mood=mood, thought=thought)

    return chat.invoke(messages)


from langchain_community.document_loaders import TextLoader

loader = TextLoader("./index.md")
loader.load()

if __name__ == "__main__":
    chatt = initialize_langchain()
    print("LangChain LLM initialized:", chatt)
