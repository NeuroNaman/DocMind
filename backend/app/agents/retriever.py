# """
# Retriever Agent - Retrieves relevant documents.
# Performs similarity search against vector store.
# """

# from typing import Any, Dict

# from app.agents.base import BaseAgent
# from app.config import get_config
# from app.core.state import AgentState
# from app.services.vector_store import get_vector_store


# class RetrieverAgent(BaseAgent):
#     """
#     Retrieves relevant document chunks from vector store.
#     Uses similarity search to find most relevant context.
#     """

#     def __init__(self):
#         super().__init__()
#         config = get_config()
#         self.k = config.RETRIEVAL_K

#     def execute(self, state: AgentState) -> Dict[str, Any]:
#         """
#         Retrieve relevant documents for the query.

#         Args:
#             state: Current agent state

#         Returns:
#             State updates with retrieved context
#         """
#         question = state.get("input", "")

#         if not question:
#             self.logger.warning("No query provided")
#             return {"context": [], "next_agent": "llm_answer_agent"}

#         try:
#             vector_store = get_vector_store()

#             # Perform similarity search
#             relevant_chunks = vector_store.similarity_search(query=question, k=self.k)

#             # Extract content from chunks
#             context = [chunk.page_content for chunk in relevant_chunks]

#             self.logger.info(f"Retrieved {len(context)} relevant chunks for query")

#             # Log retrieved sources for debugging
#             sources = [
#                 chunk.metadata.get("source", "unknown") for chunk in relevant_chunks
#             ]
#             self.logger.debug(f"Sources: {sources}")

#             return {
#                 "context": context,
#                 "next_agent": "llm_answer_agent",
#                 "metadata": {"chunks_retrieved": len(context), "sources": sources},
#             }

#         except Exception as e:
#             self.logger.error(f"Retrieval failed: {e}")
#             return {
#                 "context": [],
#                 "next_agent": "fallback_agent",
#                 "error": f"Retrieval failed: {str(e)}",
#             }


# # Standalone function for LangGraph compatibility
# def retriever_agent(state: AgentState) -> Dict[str, Any]:
#     """Standalone function wrapper for LangGraph."""
#     agent = RetrieverAgent()
#     return agent(state)


"""
Retriever Agent - Retrieves relevant documents.
Performs similarity search against vector store.
"""

# from typing import Any, Dict

# from app.agents.base import BaseAgent
# from app.config import get_config
# from app.core.state import AgentState
# from app.services.vector_store import get_vector_store


# class RetrieverAgent(BaseAgent):
#     """
#     Retrieves relevant document chunks from vector store.
#     Uses similarity search with score threshold.
#     """

#     def __init__(self):
#         super().__init__()
#         config = get_config()
#         self.k = config.RETRIEVAL_K

#         # similarity threshold (lower = better match)
#         self.similarity_threshold = 2.0

#     def execute(self, state: AgentState) -> Dict[str, Any]:
#         """
#         Retrieve relevant documents for the query.
#         """

#         question = state.get("input", "")

#         if not question:
#             self.logger.warning("No query provided")
#             return {"context": [], "next_agent": "fallback_agent"}

#         try:
#             vector_store = get_vector_store()

#             # similarity search with scores
#             results = vector_store.similarity_search_with_score(
#                 query=question,
#                 k=self.k
#             )

#             relevant_chunks = []
#             sources = []

#             for chunk, score in results:

#                 # log score for debugging
#                 self.logger.debug(f"Similarity score: {score}")

#                 if score <= self.similarity_threshold:
#                     relevant_chunks.append(chunk)
#                     sources.append(chunk.metadata.get("source", "unknown"))

#             context = [chunk.page_content for chunk in relevant_chunks]

#             # if nothing relevant → fallback
#             if not context:
#                 self.logger.info("No relevant chunks found using fallback agent")

#                 return {
#                     "context": [],
#                     "next_agent": "fallback_agent",
#                     "metadata": {"chunks_retrieved": 0},
#                 }

#             self.logger.info(f"Retrieved {len(context)} relevant chunks")

#             return {
#                 "context": context,
#                 "next_agent": "llm_answer_agent",
#                 "metadata": {
#                     "chunks_retrieved": len(context),
#                     "sources": sources,
#                 },
#             }

#         except Exception as e:
#             self.logger.error(f"Retrieval failed: {e}")

#             return {
#                 "context": [],
#                 "next_agent": "fallback_agent",
#                 "error": f"Retrieval failed: {str(e)}",
#             }


# # LangGraph wrapper
# def retriever_agent(state: AgentState) -> Dict[str, Any]:
#     """Standalone function wrapper for LangGraph."""
#     agent = RetrieverAgent()
#     return agent(state)

"""
Retriever Agent - Retrieves relevant documents.
Performs similarity search against vector store with score filtering.
"""

# from typing import Any, Dict, List

# from app.agents.base import BaseAgent
# from app.config import get_config
# from app.core.state import AgentState
# from app.services.vector_store import get_vector_store


# class RetrieverAgent(BaseAgent):
#     """
#     Retrieves relevant document chunks from vector store.
#     Uses similarity search with distance threshold filtering.
#     """

#     def __init__(self):
#         super().__init__()

#         config = get_config()

#         # number of chunks to retrieve
#         self.k = config.RETRIEVAL_K

#         # Chroma returns cosine distance (lower = better)
#         # good matches usually < 1.2
#         self.similarity_threshold = 1.8

#     def execute(self, state: AgentState) -> Dict[str, Any]:
#         """
#         Retrieve relevant documents for the query.
#         """

#         question = state.get("input", "")

#         if not question:
#             self.logger.warning("No query provided")

#             return {
#                 "context": [],
#                 "next_agent": "fallback_agent",
#             }

#         try:
#             vector_store = get_vector_store()

#             # Retrieve documents with similarity score
#             results = vector_store.similarity_search_with_score(
#                 query=question,
#                 k=self.k
#             )

#             relevant_chunks: List = []
#             sources: List[str] = []

#             for chunk, score in results:

#                 # Debug score logging
#                 self.logger.debug(f"Similarity score: {score}")

#                 # Lower score = better match
#                 if score <= self.similarity_threshold:
#                     relevant_chunks.append(chunk)
#                     sources.append(chunk.metadata.get("source", "unknown"))

#             context = [chunk.page_content for chunk in relevant_chunks]

#             # If no relevant chunks → fallback
#             if not context:

#                 self.logger.info(
#                     "No relevant chunks found -> routing to fallback agent"
#                 )

#                 return {
#                     "context": [],
#                     "next_agent": "fallback_agent",
#                     "metadata": {
#                         "chunks_retrieved": 0,
#                         "sources": []
#                     },
#                 }

#             self.logger.info(
#                 f"Retrieved {len(context)} relevant chunks for query"
#             )

#             return {
#                 "context": context,
#                 "next_agent": "llm_answer_agent",
#                 "metadata": {
#                     "chunks_retrieved": len(context),
#                     "sources": sources,
#                 },
#             }

#         except Exception as e:

#             self.logger.error(f"Retrieval failed: {e}")

#             return {
#                 "context": [],
#                 "next_agent": "fallback_agent",
#                 "error": f"Retrieval failed: {str(e)}",
#             }


# # LangGraph wrapper
# def retriever_agent(state: AgentState) -> Dict[str, Any]:
#     """
#     Standalone function wrapper for LangGraph.
#     """

#     agent = RetrieverAgent()
#     return agent(state)



# from typing import Any, Dict, List

# from app.agents.base import BaseAgent
# from app.config import get_config
# from app.core.state import AgentState
# from app.services.vector_store import get_vector_store


# class RetrieverAgent(BaseAgent):
#     """
#     Retrieves relevant document chunks from vector store.
#     Uses similarity search with distance threshold filtering.
#     """

#     def __init__(self):
#         super().__init__()

#         config = get_config()

#         # number of chunks to retrieve
#         self.k = config.RETRIEVAL_K

#         # Chroma returns cosine distance (lower = better)
#         # good matches usually < 1.2
#         self.similarity_threshold = 1.3

#     def execute(self, state: AgentState) -> Dict[str, Any]:
#         """
#         Retrieve relevant documents for the query.
#         """

#         question = state.get("input", "")

#         if not question:
#             self.logger.warning("No query provided")

#             return {
#                 "context": [],
#                 "next_agent": "fallback_agent",
#             }

#         try:
#             vector_store = get_vector_store()

#             # Retrieve documents with similarity score
#             results = vector_store.similarity_search_with_score(
#                 query=question,
#                 k=self.k
#             )

#             relevant_chunks: List = []
#             sources: List[str] = []

#             for chunk, score in results:

#                 # Debug score logging
#                 self.logger.debug(f"Similarity score: {score}")

#                 # Lower score = better match
#                 if score <= self.similarity_threshold:
#                     relevant_chunks.append(chunk)
#                     sources.append(chunk.metadata.get("source", "unknown"))

#             context = [chunk.page_content for chunk in relevant_chunks]

#             # If no relevant chunks → fallback
#             if not context:

#                 self.logger.info(
#                     "No relevant chunks found -> routing to fallback agent"
#                 )

#                 return {
#                     "context": [],
#                     "next_agent": "fallback_agent",
#                     "metadata": {
#                         "chunks_retrieved": 0,
#                         "sources": []
#                     },
#                 }

#             self.logger.info(
#                 f"Retrieved {len(context)} relevant chunks for query"
#             )

#             return {
#                 "context": context,
#                 "next_agent": "llm_answer_agent",
#                 "metadata": {
#                     "chunks_retrieved": len(context),
#                     "sources": sources,
#                 },
#             }

#         except Exception as e:

#             self.logger.error(f"Retrieval failed: {e}")

#             return {
#                 "context": [],
#                 "next_agent": "fallback_agent",
#                 "error": f"Retrieval failed: {str(e)}",
#             }


# # LangGraph wrapper
# def retriever_agent(state: AgentState) -> Dict[str, Any]:
#     """
#     Standalone function wrapper for LangGraph.
#     """

#     agent = RetrieverAgent()
#     return agent(state)


from typing import Any, Dict, List

from app.agents.base import BaseAgent
from app.config import get_config
from app.core.state import AgentState
from app.services.vector_store import get_vector_store


class RetrieverAgent(BaseAgent):
    """
    Retrieves relevant document chunks from vector store.
    Uses similarity search with relaxed threshold filtering.
    """

    def __init__(self):
        super().__init__()

        config = get_config()

        # number of chunks to retrieve
        self.k = config.RETRIEVAL_K

        # relaxed similarity threshold
        # Chroma cosine distance: lower = better
        self.similarity_threshold = 1.8

    def execute(self, state: AgentState) -> Dict[str, Any]:

        question = state.get("input", "")

        if not question:
            self.logger.warning("No query provided")

            return {
                "context": [],
                "next_agent": "fallback_agent",
            }

        try:

            vector_store = get_vector_store()

            results = vector_store.similarity_search_with_score(
                query=question,
                k=self.k
            )

            relevant_chunks: List = []
            sources: List[str] = []
            scores: List[float] = []

            for chunk, score in results:

                self.logger.debug(f"Similarity score: {score}")

                scores.append(score)

                # relaxed filtering
                if score <= self.similarity_threshold:
                    relevant_chunks.append(chunk)
                    sources.append(chunk.metadata.get("source", "unknown"))

            # ------------------------------------------------
            # SAFETY: if nothing passes threshold
            # return top chunks anyway
            # ------------------------------------------------
            if not relevant_chunks and results:

                self.logger.warning(
                    "No chunks passed threshold -> returning top results"
                )

                for chunk, score in results[:2]:
                    relevant_chunks.append(chunk)
                    sources.append(chunk.metadata.get("source", "unknown"))
                    scores.append(score)

            context = [chunk.page_content for chunk in relevant_chunks]

            if not context:

                self.logger.info(
                    "Retriever found no useful chunks -> fallback"
                )

                return {
                    "context": [],
                    "next_agent": "fallback_agent",
                    "metadata": {
                        "chunks_retrieved": 0,
                        "sources": [],
                        "avg_score": None
                    },
                }

            avg_score = sum(scores) / len(scores) if scores else None

            self.logger.info(
                f"Retrieved {len(context)} relevant chunks for query"
            )

            return {
                "context": context,
                "next_agent": "llm_answer_agent",
                "metadata": {
                    "chunks_retrieved": len(context),
                    "sources": sources,
                    "avg_score": avg_score,
                },
            }

        except Exception as e:

            self.logger.error(f"Retrieval failed: {e}")

            return {
                "context": [],
                "next_agent": "fallback_agent",
                "error": f"Retrieval failed: {str(e)}",
            }


# LangGraph wrapper
def retriever_agent(state: AgentState) -> Dict[str, Any]:

    agent = RetrieverAgent()
    return agent(state)