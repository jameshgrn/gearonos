from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .problem_solving import problem_solving_chain
from .reflection_introspection import reflection_introspection_chain
from .hypothesis_generation import hypothesis_generation_chain
from .critique_agent import CritiqueAgent

class Orchestrator:
    def __init__(self):
        # Initialize any required components or state
        self.critique_agent = CritiqueAgent()

    def generate_meta_prompt(self, input_text):
        # Here we define the logic to generate meta-prompts
        # For simplicity, we'll just prepend a statement to clarify the task
        meta_prompt = "GearonOS, you are an advanced AI capable of solving complex problems, reflecting on deep topics, and generating hypotheses. Your task is to: " + input_text
        return meta_prompt

    def orchestrate(self, input_text):
        # Use the generate_meta_prompt method to improve the input prompt
        meta_prompt = self.generate_meta_prompt(input_text)
        # Determine the type of input and which chain to invoke
        if "solve" in meta_prompt:
            initial_decision = problem_solving_chain
        elif "reflect" in meta_prompt:
            initial_decision = reflection_introspection_chain
        elif "hypothesize" in meta_prompt:
            initial_decision = hypothesis_generation_chain
        else:
            # Default response or action
            return "I am not sure how to process this input."
        
        # Invoke the critique agent to refine the decision
        refined_decision, reasoning = self.critique_agent.critique_and_refine_decision(initial_decision, meta_prompt)
        
        # Execute the refined decision
        return refined_decision(meta_prompt), reasoning

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
    print("Result:", reflection_result)
    
    # Test input for hypothesis generation
    hypothesis_input = "hypothesize: What if humans could photosynthesize like plants?"
    hypothesis_result = orchestrator.orchestrate(hypothesis_input)
    print("\nTest Orchestrator - Hypothesis Generation:")
    print("Input:", hypothesis_input)
    print("Result:", hypothesis_result)
