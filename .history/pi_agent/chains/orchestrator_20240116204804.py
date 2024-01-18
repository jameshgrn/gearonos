from .problem_solving import problem_solving_chain
from .reflection_introspection import reflection_introspection_chain
from .hypothesis_generation import hypothesis_generation_chain

class Orchestrator:
    def __init__(self):
        # Initialize any required components or state
        pass

    def orchestrate(self, input_text):
        # Determine the type of input and which chain to invoke
        if "solve" in input_text:
            return problem_solving_chain(input_text)
        elif "reflect" in input_text:
            return reflection_introspection_chain(input_text)
        elif "hypothesize" in input_text:
            return hypothesis_generation_chain(input_text)
        else:
            # Default response or action
            return "I am not sure how to process this input."

# Example usage of the Orchestrator
if __name__ == '__main__':
    orchestrator = Orchestrator()
    input_text = "I want to solve a puzzle."
    result = orchestrator.orchestrate(input_text)

