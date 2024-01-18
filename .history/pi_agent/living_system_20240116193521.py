from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import json

# Initialize the LLaMA model with the correct model path
llm = LlamaCpp(
    model_path="/Users/jakegearon/Downloads/starling-lm-7b-alpha.Q4_K_S.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
)

# Memory system functions
memory_file = 'pi_agent/memories.json'

def save_thought(thought):
    if not os.path.exists(memory_file):
        with open(memory_file, 'w') as file:
            json.dump([], file)

