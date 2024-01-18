from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize the LLaMA model with the correct model path
llm = LlamaCpp(
    model_path="/path/to/your/model/file.bin",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    # Add other parameters as needed
)

# Create a prompt template
template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Create an LLMChain instance
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Example question
question = "What is the capital of France?"
result = llm_chain.run(question)
print(result)