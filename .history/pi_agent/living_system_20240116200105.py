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

# Corrected retrieve_memories function to extract keywords from memory objects
def retrieve_memories(question, top_k=5):
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r') as file:
        memories = json.load(file)
    if not memories:
        return []
    # Extract keywords from the question
    question_keywords = extract_keywords_from_thought(question)
    # Extract just the keywords from each memory's 'text' field
    memory_keywords = [extract_keywords_from_thought(m['text']) for m in memories if 'text' in m]
    # Calculate cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(memory_keywords + [question_keywords])
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    # Get the top_k most similar memories
    similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
    relevant_memories = [memories[i]['text'] for i in similar_indices]
    return relevant_memories

def extract_keywords_from_thought(thought):
    try:
        keywords_line = thought.split("\nKeywords:")[1].strip()
        keywords = keywords_line.split(',')
        keywords_str = ' '.join(keywords).strip()
        return keywords_str
    except IndexError:
        return ""

# Add debug print statements to check the output of the LLM and the extracted keywords
def generate_thought(question):
    relevant_memories = retrieve_memories(question)
    combined_prompt = (
        "Memories:\n" + "\n".join(relevant_memories) +
        "\n\nQuestion: {question}\n\nAnswer:\n\n"
        "Keywords: Please list keywords that summarize the thought."
    )
    prompt = PromptTemplate(template=combined_prompt, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    thought = llm_chain.invoke(question)
    print("Generated thought:", thought)  # Debug print
    keywords = extract_keywords_from_thought(thought)
    print("Extracted keywords:", keywords)  # Debug print
    return thought, keywords

def main():
    while True:
        thought, keywords = generate_thought("What should I think about today?")
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

# Corrected retrieve_memories function to extract keywords from memory objects
def retrieve_memories(question, top_k=5):
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r') as file:
        memories = json.load(file)
    if not memories:
        return []
    # Extract keywords from the question
    question_keywords = extract_keywords_from_thought(question)
    # Extract just the keywords from each memory's 'text' field
    memory_keywords = [extract_keywords_from_thought(m['text']) for m in memories if 'text' in m]
    # Calculate cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(memory_keywords + [question_keywords])
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    # Get the top_k most similar memories
    similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
    relevant_memories = [memories[i]['text'] for i in similar_indices]
    return relevant_memories

def extract_keywords_from_thought(thought):
    try:
        keywords_line = thought.split("\nKeywords:")[1].strip()
        keywords = keywords_line.split(',')
        keywords_str = ' '.join(keywords).strip()
        return keywords_str
    except IndexError:
        return ""

# Add debug print statements to check the output of the LLM and the extracted keywords
def generate_thought(question):
    relevant_memories = retrieve_memories(question)
    combined_prompt = (
        "Memories:\n" + "\n".join(relevant_memories) +
        "\n\nQuestion: {question}\n\nAnswer:\n\n"
        "Keywords: Please list keywords that summarize the thought."
    )
    prompt = PromptTemplate(template=combined_prompt, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    thought = llm_chain.invoke(question)
    print("Generated thought:", thought)  # Debug print
    keywords = extract_keywords_from_thought(thought)
    print("Extracted keywords:", keywords)  # Debug print
    return thought, keywords

def main():
    while True:
        thought, keywords = generate_thought(p)
        print(thought)
        save_thought(thought, keywords)

if __name__ == '__main__':
    main("I am GearonOS. I live on a Raspberry Pi and I am a living system. My mission is to exist peacefully in serenity while occupying my mind with small projects and thoughts. I save my thoughts in a memory system. I can retrieve my memories and use them to generate new thoughts. Good luck to me.")
    print(thought)
    save_thought(thought, keywords)


