from langchain.llms import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os

# Assuming the memory system functions and LLM initialization are available from living_system.py
from ..living_system import save_thought, retrieve_memories, llm

memory_file = 'pi_agent/memories.json'

def reflection_introspection_chain(reflection_topic):
    # Retrieve relevant memories to provide context for the reflection
    relevant_memories = retrieve_memories(reflection_topic)
    memory_context = "\\n".join(relevant_memories)

    # Construct the reflection prompt
    prompt_template = PromptTemplate(template='''\
Memories:
{memory_context}

Reflection: Reflect on the following thought or experience from your memory: {reflection_topic}
GearonOS, consider how this has influenced your understanding or behavior. What have you learned, and how has it shaped your development?

Insights:
''', input_variables=["memory_context", "reflection_topic"])

    # Create an LLMChain instance
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)

    # Invoke the LLM to generate insights
    response = llm_chain.invoke(memory_context=memory_context, reflection_topic=reflection_topic)
    print("Generated insights:", response)  # Debug print

    # Save the insights in the memory system
    if isinstance(response, dict) and 'text' in response:
        insights_text = response['text']
        # Extract keywords or a summary for the memory system
        insights_summary = extract_keywords_from_thought(insights_text)
        save_thought(insights_text, insights_summary)

    return response

# Helper function to extract keywords or a summary from the insights text
def extract_keywords_from_thought(text):
    # Implement keyword extraction logic here
    # For now, we'll just return the first line as a summary
    return text.splitlines()[0] if text else ""

# Example usage of the reflection_introspection_chain
if __name__ == '__main__':
    reflection_topic = "The importance of curiosity in learning and development."
    insights = reflection_introspection_chain(reflection_topic)
    print(insights)
""")