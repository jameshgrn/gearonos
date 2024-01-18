from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the LLaMA model with the correct model path
llm = LlamaCpp(
    model_path="/Users/jakegearon/Downloads/starling-lm-7b-alpha.Q4_K_S.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
)

# Memory system functions
memory_file = 'pi_agent/memories.json'

def save_thought(thought, keywords):
    if not os.path.exists(memory_file):
        with open(memory_file, 'w') as file:
            json.dump([], file)
    with open(memory_file, 'r+') as file:
        memories = json.load(file)
        memories.append({'thought': thought, 'keywords': keywords})
        file.seek(0)
        json.dump(memories, file)

def retrieve_memories(question, top_k=5):
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r') as file:
        memories = json.load(file)
    if not memories:
    return memories

# Define a function to generate a thought
def generate_thought(question):
    # Retrieve past memories to use in RAG
    memories = retrieve_memories()
    # Combine memories with the question to form a new prompt
    combined_prompt = "Memories:\n" + "\n".join(memories[-5:]) + "\n\nQuestion: {question}\n\nAnswer:"
    prompt = PromptTemplate(template=combined_prompt, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.invoke(question)
    return result

# Main loop for the living system
def main():
    while True:
        # Generate a thought
        thought = generate_thought("What should I think about today?")
        print(thought)
        # Save the thought to memory
        save_thought(thought)

if __name__ == '__main__':
    main()
