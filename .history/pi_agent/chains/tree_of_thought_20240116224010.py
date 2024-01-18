from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
import os



# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm
from ..chains.keyword_extractor import KeywordExtractor
from langchain_experimental.tot.base import ToTChain
import re
from typing import Tuple
from langchain_experimental.tot.checker import ToTChecker
from langchain_experimental.tot.thought import ThoughtValidity

# Define a custom checker class for the Tree of Thoughts
class MyChecker(ToTChecker):
    def evaluate(
        self, problem_description: str, thoughts: Tuple[str, ...] = ()
    ) -> ThoughtValidity:
        last_thought = thoughts[-1]
        clean_solution = last_thought.replace(" ", "").replace('"', "")
        regex_solution = clean_solution.replace("*", ".").replace("|", "\\|")
        # Assuming sudoku_solution is a predefined correct solution
        if sudoku_solution in clean_solution:
            return ThoughtValidity.VALID_FINAL
        elif re.search(regex_solution, sudoku_solution):
            return ThoughtValidity.VALID_INTERMEDIATE
        else:
            return ThoughtValidity.INVALID

memory_file = 'pi_agent/memories.json'

# Initialize the ToTChain with the custom checker
tot_chain = ToTChain(
    llm=llm, checker=MyChecker(), k=30, c=5, verbose=True, verbose_llm=False
)

# Example usage of the ToTChain with the invoke method
def tree_of_thought_chain(problem_description):
    response = tot_chain.invoke({"problem_description": problem_description})
    return {
        "input_text": problem_description,
        "tree_of_thoughts": response
    }

# Sample problem description for testing
problem_description = "Explore the concept of consciousness in artificial intelligence."

# Invoke the tree_of_thought_chain function with the problem description
result = tree_of_thought_chain(problem_description)

# Display the result
print("Tree of Thought Chain Result:")
print(result)