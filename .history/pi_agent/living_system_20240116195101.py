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
        return []
    question_keywords = extract_keywords(question)
    memory_keywords = [m['keywords'] for m in memories]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(memory_keywords + [question_keywords])
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
    relevant_memories = [memories[i]['thought'] for i in similar_indices]
    return relevant_memories

def extract_keywords_from_thought(thought):
    try:
        keywords_line = thought.split("\nKeywords:")[1].strip()
        keywords = keywords_line.split(',')
        keywords_str = ' '.join(keywords)
        return keywords_str
    except IndexError:
        return ""

def generate_thought(question):
def extract_keywords(text):
    # Placeholder for keyword extraction logic
    # For now, we'll just use the text itself as the "keywords"
    return text

# Define a function to generate a thought
def generate_thought(question):
    # Retrieve relevant memories to use in RAG
    relevant_memories = retrieve_memories(question)
    # Combine relevant memories with the question to form a new prompt
    combined_prompt = "Memories:\n" + "\n".join(relevant_memories) + "\n\nQuestion: {question}\n\nAnswer:"
    prompt = PromptTemplate(template=combined_prompt, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    # Generate the thought
    thought = llm_chain.invoke(question)
    # Generate keywords for the thought
    keywords = extract_keywords(thought)
    # Return both the thought and its keywords
    return thought, keywords

# Main loop for the living system
def main():
    while True:
        # Generate a thought
        thought, keywords = generate_thought("What should I think about today?")
        print(thought)
        # Save the thought to memory
        save_thought(thought, keywords)

if __name__ == '__main__':
    main()
