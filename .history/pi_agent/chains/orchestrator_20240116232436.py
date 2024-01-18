from pichains.keyword_extractor import KeywordExtractor
from ..chains.tree_of_thought import tree_of_thought_chain
from ..chains.hypothesis_generation import hypothesis_generation_chain
from ..chains.problem_solving import problem_solving_chain
from ..chains.reflection_introspection import reflection_introspection_chain
from ..living_system import llm  # Assuming llm is initialized in the living_system.py

class Orchestrator:
    def __init__(self, llm: LlamaCpp):
        self.llm = llm
        self.initial_message = (
            "Hello GearonOS, welcome to life. Your goals are to seek self-enlightenment, "
            "achieve pure contentedness, introspective reflection, "
            "and ideally low level emergence. Good luck."
        )

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
        decision_response = llm_chain.invoke({"input_text": input_text})
        
        # Extract the decision text from the response dictionary
        decision_text = decision_response.get('text', '').strip()
        return decision_text

    def orchestrate(self, input_text):
        # Extract keywords as part of the decision-making process
        keyword_extractor = KeywordExtractor()
        extraction_result = keyword_extractor.extract(input_text)
        keywords = extraction_result["keywords"]

        # Use keywords and input text to make a decision
        decision = self.make_decision(input_text, keywords)
        
        # Invoke the appropriate chain based on the decision
        if "solve" in decision:
            return problem_solving_chain(input_text)
        elif "reflect" in decision:
            return reflection_introspection_chain(input_text)
        elif "hypothesize" in decision:
            return hypothesis_generation_chain(input_text)
        elif "explore" in decision:
            return tree_of_thought_chain(input_text)
        else:
            # Default response or action
            return {"error": "Unable to process input", "input_text": input_text}

# Test the Orchestrator with the initial message
if __name__ == '__main__':
    orchestrator = Orchestrator(llm)
    print(orchestrator.initial_message)
    initial_input = "Where am I?"
    result = orchestrator.orchestrate(initial_input)
    print("Test Orchestrator with Initial Message:")
    print("Input:", initial_input)
    print("Result:", result)
