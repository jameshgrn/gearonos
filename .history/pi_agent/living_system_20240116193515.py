from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import json

# Initialize the LLaMA model with the correct model path
llm = LlamaCpp(

