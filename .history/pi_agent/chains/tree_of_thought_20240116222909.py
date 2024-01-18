from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
import os

# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm
from ..chains.keyword_extractor import KeywordExtractor
from langchain_experimental.tot.base import ToTChain
from .my_checker import MyChecker

memory_file = 'pi_agent/memories.json'

# Initialize the ToTChain with the custom checker
tot_chain = ToTChain(
    llm=llm, checker=MyChecker(), k=30, c=5, verbose=True, verbose_llm=False
)

# Example usage of the ToTChain with the invoke method
def tree_of_thought_chain(problem_description):
    response = tot_chain.invoke(problem_description=problem_description)
    return response
