from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
import os

# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm
from ..chains.keyword_extractor import KeywordExtractor

memory_file = 'pi_agent/memories.json'

def tree_of_thought_chain(input_text):
    # Instantiate the KeywordExtractor
    keyword_extractor = KeywordExtractor()
    
    # Retrieve relevant memories to provide context for the tree of thought
    relevant_memories = retrieve_memories(input_text)
    memory_context = "\n".join(relevant_memories)

    # Construct the tree of thought prompt
    prompt_template = PromptTemplate(template='''Memories:
{memory_context}

Thought Process:
Given the input "{input_text}", construct a tree of thoughts that explores different facets of the topic and possible conclusions.

Tree of Thoughts:
''', input_variables=["memory_context", "input_text"])

    # Create an LLMChain instance
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)

    # Invoke the LLM to generate a tree of thoughts
    response = llm_chain.invoke({"memory_context": memory_context, "input_text": input_text})
    print("Generated Tree of Thoughts:", response)  # Debug print

    # Save the tree of thoughts in the memory system

