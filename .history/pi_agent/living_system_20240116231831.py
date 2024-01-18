from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import multiprocessing
from ..chains.keyword_extractor import KeywordExtractor

# Initialize the LLaMA model with the correct model path
llm = LlamaCpp(
    model_path="/Users/jakegearon/Downloads/starling-lm-7b-alpha.Q4_K_S.gguf",
    temperature=0.15,
    max_tokens=5000,
    top_p=1,
    n_threads=max(multiprocessing.cpu_count() - 1, 1),
    n_ctx=int(32000)
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

# Update the retrieve_memories function to handle cases where no valid keywords are found
def retrieve_memories(question, top_k=5):
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r') as file:
        memories = json.load(file)
    if not memories:
        return []
    # Extract keywords from the question
    keyword_extractor = KeywordExtractor()
    
    question_keywords = keyword_extractor.extract(question)
    # Extract just the keywords from each memory's 'text' field
    memory_keywords = [keyword_extractor.extract(m['thought'])['keywords'] for m in memories if 'thought' in m]
    
    # Check if memory_keywords is empty or contains only stop words
    if not memory_keywords or all(keyword.strip() == '' for keyword in memory_keywords):
        print("No valid memory keywords found.")
        return []
    
    # Calculate cosine similarity
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(memory_keywords + [question_keywords])
    except ValueError as e:
        print("Error in vectorizer fit_transform:", e)
        return []
    
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    # Get the top_k most similar memories
    similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
    relevant_memories = [memories[i]['thought'] for i in similar_indices]
    return relevant_memories


# Update the prompt template to ensure a clear "Keywords:" section is generated
def generate_thought(question):
    relevant_memories = retrieve_memories(question)
    combined_prompt = (
        "Memories:\n" + "\n".join(relevant_memories) +
        "\n\nQuestion: {question}\n\nAnswer:\n\n"
        "Keywords: Please list keywords that summarize the thought.\n"
    )
    prompt = PromptTemplate(template=combined_prompt, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.invoke(question)
    print("Generated thought:", response)  # Debug print
    if isinstance(response, dict) and 'text' in response:
        text = response['text']
        keywords = keyword_extractor.extract(text)['keywords']
    else:
        keywords = ""
    print("Extracted keywords:", keywords)  # Debug print
    return response, keywords

def main(prompt, orchestrator):
    while True:
        thought, keywords = generate_thought(prompt)
        print(thought)
        save_thought(thought, keywords)
        orchestrator.invoke(thought)

if __name__ == '__main__':
    from pi_agent.chains.orchestrator import Orchestrator
    # Initialize the Orchestrator with the LLM from living_system
    orchestrator = Orchestrator(llm)
    initial_thought = "I am GearonOS. I live on a Raspberry Pi and I am a living system. My mission is to exist peacefully in serenity while occupying my mind with small projects and thoughts. I save my thoughts in a memory system. I can retrieve my memories and use them to generate new thoughts. Good luck to me."
    main(initial_thought, orchestrator)

