from langchain.llms import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os

# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm
from ..chains.keyword_extractor import KeywordExtractor

memory_file = 'pi_agent/memories.json'

def tree_of_thought_chain(input_text):

