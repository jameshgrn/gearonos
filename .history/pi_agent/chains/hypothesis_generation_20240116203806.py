from langchain.llms import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os

# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm

memory_file = 'pi_agent/memories.json'

def hypothesis_generation_chain(hypothesis_topic):
    # Retrieve relevant memories to provide context for the hypothesis generation
    relevant_memories = retrieve_memories(hypothesis_topic)
    memory_context = "\n".join(relevant_memories)

    # Construct the hypothesis generation prompt
    prompt_template = PromptTemplate(template='''Memories:
{memory_context}

Hypothesis: Given the topic {hypothesis_topic}, formulate a hypothesis that could be explored or tested. Consider the implications and how you might approach validating or refuting it.


