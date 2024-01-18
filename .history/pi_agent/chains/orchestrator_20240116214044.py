from langchain.llms import LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .problem_solving import problem_solving_chain
from .reflection_introspection import reflection_introspection_chain
from .hypothesis_generation import hypothesis_generation_chain
from ..living_system import llm  # Assuming llm is initialized in the living_system.py

class Orchestrator:
    def __init__(self, llm: LLM):
        self.llm = llm

    def generate_decision_prompt(self, input_text):
        # Generate a meta-prompt to help decide which chain to use
        prompt_template = PromptTemplate(template='''
        Analyze the following input and determine the most appropriate action:
        Input: "{input_text}"
        Should we solve a problem, reflect on a topic, or generate a hypothesis? Provide your reasoning.
        Decision:
        ''', input_variables=["input_text"])
        return prompt_template

    def make_decision(self, input_text):
        # Use the LLM to make a decision on which chain to invoke
        decision_prompt = self.generate_decision_prompt(input_text)
        llm_chain = LLMChain(prompt=decision_prompt, llm=self.llm)
        decision = llm_chain.invoke(input_text=input_text)
        return decision.strip()

    def orchestrate(self, input_text):
        # Use the make_decision method to determine which chain to invoke
        decision = self.make_decision(input_text)
        if "solve" in decision:
            return problem_solving_chain(input_text)
        elif "reflect" in decision:
            return reflection_introspection_chain(input_text)
        elif "hypothesize" in decision:
            return hypothesis_generation_chain(input_text)
        else:
            # Default response or action
            return "I am not sure how to process this input."

# Test the Orchestrator with different types of input
if __name__ == '__main__':
    orchestrator = Orchestrator()
    
    # Test input for problem-solving
    problem_input = "solve: Calculate the area of a circle with a radius of 5 units."
    problem_result = orchestrator.orchestrate(problem_input)
    print("Test Orchestrator - Problem-Solving:")
    print("Input:", problem_input)
    print("Result:", problem_result)
    
    # Test input for reflection and introspection
    reflection_input = "reflect: Consider the role of curiosity in personal growth."
    reflection_result = orchestrator.orchestrate(reflection_input)
    print("\nTest Orchestrator - Reflection and Introspection:")
    print("Input:", reflection_input)
from langchain.llms import LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .problem_solving import problem_solving_chain
from .reflection_introspection import reflection_introspection_chain
from .hypothesis_generation import hypothesis_generation_chain
from ..living_system import llm  # Assuming llm is initialized in the living_system.py

class Orchestrator:
    def __init__(self, llm: LLM):
        self.llm = llm

    def generate_decision_prompt(self, input_text):
        # Generate a meta-prompt to help decide which chain to use
        prompt_template = PromptTemplate(template='''
        Analyze the following input and determine the most appropriate action:
        Input: "{input_text}"
        Should we solve a problem, reflect on a topic, or generate a hypothesis? Provide your reasoning.
        Decision:
        ''', input_variables=["input_text"])
        return prompt_template

    def make_decision(self, input_text):
        # Use the LLM to make a decision on which chain to invoke
        decision_prompt = self.generate_decision_prompt(input_text)
        llm_chain = LLMChain(prompt=decision_prompt, llm=self.llm)
        decision = llm_chain.invoke(input_text=input_text)
        return decision.strip()

    def orchestrate(self, input_text):
        # Use the make_decision method to determine which chain to invoke
        decision = self.make_decision(input_text)
    print("Result:", reflection_result)
    
    # Test input for hypothesis generation
    hypothesis_input = "hypothesize: What if humans could photosynthesize like plants?"
    hypothesis_result = orchestrator.orchestrate(hypothesis_input)
    print("\nTest Orchestrator - Hypothesis Generation:")
    print("Input:", hypothesis_input)
    print("Result:", hypothesis_result)
