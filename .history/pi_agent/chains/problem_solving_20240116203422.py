from langchain.llms import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os

# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm

memory_file = 'pi_agent/memories.json'

def problem_solving_chain(problem_statement):
    # Retrieve relevant memories to provide context for the problem-solving
    relevant_memories = retrieve_memories(problem_statement)
    memory_context = "\n".join(relevant_memories)

    # Construct the problem-solving prompt
    prompt_template = PromptTemplate(template='''\
Memories:
{memory_context}

Problem: {problem_statement}
GearonOS, please analyze the problem and provide a step-by-step solution. Consider different approaches and explain your reasoning.

Solution:
''', input_variables=["memory_context", "problem_statement"])

    # Create an LLMChain instance
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)

    # Invoke the LLM to generate a solution
    response = llm_chain.invoke(memory_context=memory_context, problem_statement=problem_statement)
    print("Generated solution:", response)  # Debug print

    # Save the solution in the memory system
    if isinstance(response, dict) and 'text' in response:
        solution_text = response['text']

