from langchain.llms import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os
from ..chains.keyword_extractor import KeywordExtractor

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
        # Extract keywords or a summary for the memory system
        solution_summary = extract_keywords_from_thought(solution_text)
        save_thought(solution_text, solution_summary)

    return response

# Helper function to extract keywords or a summary from the solution text
def extract_keywords_from_thought(text):
    extractor = KeywordExtractor()
    return extractor.extract_keywords(text)

    # Implement keyword extraction logic here
    # For now, we'll just return the first line as a summary
    return text.splitlines()[0] if text else ""

# Example usage of the problem_solving_chain
if __name__ == '__main__':
    problem_statement = "A farmer has 17 sheep, all but 9 die. How many are left alive?"
    solution = problem_solving_chain(problem_statement)
    print(solution)
