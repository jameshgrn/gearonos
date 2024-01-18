from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
import os
from ..chains.keyword_extractor import KeywordExtractor

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

Proposed Hypothesis:
''', input_variables=["memory_context", "hypothesis_topic"])

    # Create an LLMChain instance
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)

    # Invoke the LLM to generate a hypothesis
    response = llm_chain.invoke(memory_context=memory_context, hypothesis_topic=hypothesis_topic)
    print("Generated hypothesis:", response)  # Debug print

    # Save the hypothesis in the memory system
    if isinstance(response, dict) and 'text' in response:
        hypothesis_text = response['text']
        # Extract keywords or a summary for the memory system
        hypothesis_summary = extract_keywords_from_thought(hypothesis_text)
        save_thought(hypothesis_text, hypothesis_summary)

    return response

# Helper function to extract keywords or a summary from the hypothesis text
def extract_keywords_from_thought(text):
    extractor = KeywordExtractor()
    return extractor.extract_keywords(text)

# Test the hypothesis_generation_chain function
if __name__ == '__main__':
    hypothesis_topic = "What signals of th."
    hypothesis = hypothesis_generation_chain(hypothesis_topic)
    print("Test Hypothesis Generation Chain:")
    print("Hypothesis Topic:", hypothesis_topic)
    print("Generated Hypothesis:", hypothesis)
