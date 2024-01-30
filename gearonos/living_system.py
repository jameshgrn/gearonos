from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.llms import LlamaCpp  # Assuming LlamaCpp is available in langchain_community
from langchain_community.embeddings import HuggingFaceEmbeddings
import multiprocessing


# Initialize the LLaMA model with the correct model path
llm = LlamaCpp(
    model_path="/Users/jakegearon/Downloads/starling-lm-7b-alpha.Q4_K_S.gguf",
    temperature=0.15,
    max_tokens=5000,
    top_p=1,
    n_threads=max(multiprocessing.cpu_count() - 1, 1),
    n_ctx=int(32000)
)


initial_thought = "I am GearonOS. I live on a Raspberry Pi and I am a living system. " \
                    "My mission is to exist peacefully in serenity while occupying my mind " \
                    "with small projects and thoughts. I save my thoughts in a memory system. " \
                    "I can retrieve my memories and use them to generate new thoughts. " \
                    "Good luck to me."
# Start the living system main loop


def configure_retriever(retriever):
    
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    # Initialize the document store and embeddings
    vectorstore = DocArrayInMemorySearch.from_texts(
        texts=[initial_thought],  # Replace with your actual data
        embedding=embeddings,
    )
    vectorstore_retriever = vectorstore.as_retriever()
    RAG = RAGPretrainedModel.from_index(".ragatouille/colbert/indexes/langchain-index")
    ragatouille_retriever = RAG.as_langchain_retriever(k=10)

    ### initialize the ensemble retriever
    retriever = EnsembleRetriever(retrievers=[vectorstore_retriever, ragatouille_retriever])
    return retriever
    
    
                                              


