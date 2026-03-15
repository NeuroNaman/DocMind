# """
# LLM service for language model operations.
# Provides abstraction over LLM providers.
# """

# from typing import Dict, List, Optional

# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq

# from app.config import get_config
# from app.exceptions import LLMError
# from app.utils.logger import get_logger

# logger = get_logger("llm_service")


# class LLMService:
#     """
#     Service for LLM operations.
#     Supports multiple LLM providers with a unified interface.
#     """

#     _instance: Optional["LLMService"] = None
#     _llm = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#         return cls._instance

#     def __init__(self):
#         if self._llm is None:
#             self._initialize()

#     def _initialize(self):
#         """Initialize the LLM."""
#         config = get_config()

#         try:
#             self._llm = ChatGroq(
#                 temperature=config.LLM_TEMPERATURE,
#                 model_name=config.LLM_MODEL,
#                 api_key=config.GROQ_API_KEY,
#             )
#             logger.info(f"LLM initialized: {config.LLM_MODEL}")
#         except Exception as e:
#             logger.error(f"Failed to initialize LLM: {e}")
#             raise LLMError(f"LLM initialization failed: {str(e)}")

#     @property
#     def llm(self):
#         """Get the LLM instance."""
#         return self._llm

#     def generate_answer(
#         self, question: str, context: List[str], system_prompt: str = None
#     ) -> str:
#         """
#         Generate an answer based on context.

#         Args:
#             question: User's question
#             context: List of relevant context chunks
#             system_prompt: Optional custom system prompt

#         Returns:
#             Generated answer string
#         """
#         if system_prompt is None:
#             system_prompt = (
#                 "You are a helpful assistant that answers questions based on the provided context. "
#                 "If the context doesn't contain relevant information, say so clearly. "
#                 "Be concise but comprehensive."
#             )

#         prompt = ChatPromptTemplate.from_messages(
#             [
#                 ("system", system_prompt),
#                 ("human", "Context:\n{context}\n\nQuestion: {question}"),
#             ]
#         )

#         chain = prompt | self._llm | StrOutputParser()

#         try:
#             context_str = "\n\n".join(context) if context else "No context provided"
#             answer = chain.invoke({"context": context_str, "question": question})
#             logger.info("Generated answer from LLM")
#             return answer
#         except Exception as e:
#             logger.error(f"LLM generation failed: {e}")
#             raise LLMError(f"Failed to generate answer: {str(e)}")

#     def generate_simple(self, prompt: str) -> str:
#         """
#         Generate a simple response without context.

#         Args:
#             prompt: Direct prompt to the LLM

#         Returns:
#             Generated response
#         """
#         try:
#             response = self._llm.invoke(prompt)
#             return response.content
#         except Exception as e:
#             logger.error(f"Simple generation failed: {e}")
#             raise LLMError(f"Generation failed: {str(e)}")

#     def generate_with_history(
#         self, question: str, context: List[str], history: List[Dict[str, str]]
#     ) -> str:
#         """
#         Generate answer with conversation history.

#         Args:
#             question: Current question
#             context: Relevant context chunks
#             history: List of previous messages

#         Returns:
#             Generated answer
#         """
#         messages = [
#             (
#                 "system",
#                 "You are a helpful assistant. Answer based on the context provided.",
#             )
#         ]

#         # Add history
#         for msg in history[-5:]:  # Last 5 messages
#             role = "human" if msg.get("role") == "user" else "assistant"
#             messages.append((role, msg.get("content", "")))

#         # Add current context and question
#         context_str = "\n\n".join(context) if context else "No additional context"
#         messages.append(("human", f"Context:\n{context_str}\n\nQuestion: {question}"))

#         prompt = ChatPromptTemplate.from_messages(messages)
#         chain = prompt | self._llm | StrOutputParser()

#         try:
#             return chain.invoke({})
#         except Exception as e:
#             logger.error(f"Generation with history failed: {e}")
#             raise LLMError(f"Failed to generate answer: {str(e)}")


# # Global singleton instance
# _llm_service: Optional[LLMService] = None


# def get_llm_service() -> LLMService:
#     """Get the global LLM service instance."""
#     global _llm_service
#     if _llm_service is None:
#         _llm_service = LLMService()
#     return _llm_service



"""
LLM service for language model operations.
Provides abstraction over LLM providers.
"""

from typing import Dict, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.config import get_config
from app.exceptions import LLMError
from app.utils.logger import get_logger

logger = get_logger("llm_service")


class LLMService:
    """
    Service for LLM operations.
    Supports multiple LLM providers with a unified interface.
    """

    _instance: Optional["LLMService"] = None
    _llm = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._llm is None:
            self._initialize()

    def _initialize(self):
        """Initialize the LLM."""
        config = get_config()

        try:
            self._llm = ChatGroq(
                temperature=config.LLM_TEMPERATURE,
                model_name=config.LLM_MODEL,
                api_key=config.GROQ_API_KEY,
            )

            logger.info(f"LLM initialized: {config.LLM_MODEL}")

        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise LLMError(f"LLM initialization failed: {str(e)}")

    @property
    def llm(self):
        """Get the LLM instance."""
        return self._llm

    # ------------------------------------------------
    # Context-based generation (RAG)
    # ------------------------------------------------
    def generate_answer(
        self,
        question: str,
        context: List[str],
        system_prompt: Optional[str] = None,
    ) -> str:

        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant that answers questions using ONLY the provided context.\n"
                "If the answer is not present in the context, respond exactly with:\n"
                "'The context does not contain the answer.'\n"
                "Do not hallucinate."
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Context:\n{context}\n\nQuestion: {question}"),
            ]
        )

        chain = prompt | self._llm | StrOutputParser()

        try:

            context_str = "\n\n".join(context) if context else "No context provided"

            answer = chain.invoke(
                {
                    "context": context_str,
                    "question": question,
                }
            )

            logger.info("Generated answer from LLM")

            return answer.strip()

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise LLMError(f"Failed to generate answer: {str(e)}")

    # ------------------------------------------------
    # Simple generation (no context)
    # ------------------------------------------------
    def generate_simple(self, prompt: str) -> str:

        try:

            response = self._llm.invoke(prompt)

            return response.content.strip()

        except Exception as e:
            logger.error(f"Simple generation failed: {e}")
            raise LLMError(f"Generation failed: {str(e)}")

    # ------------------------------------------------
    # Generation with chat history
    # ------------------------------------------------
    def generate_with_history(
        self,
        question: str,
        context: List[str],
        history: List[Dict[str, str]],
    ) -> str:

        messages = [
            (
                "system",
                "You are a helpful assistant that answers using the provided context.",
            )
        ]

        # Add conversation history
        for msg in history[-5:]:
            role = "human" if msg.get("role") == "user" else "assistant"
            messages.append((role, msg.get("content", "")))

        context_str = "\n\n".join(context) if context else "No additional context"

        messages.append(
            (
                "human",
                f"Context:\n{context_str}\n\nQuestion: {question}",
            )
        )

        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | self._llm | StrOutputParser()

        try:

            answer = chain.invoke({})

            return answer.strip()

        except Exception as e:
            logger.error(f"Generation with history failed: {e}")
            raise LLMError(f"Failed to generate answer: {str(e)}")


# ------------------------------------------------
# Global singleton instance
# ------------------------------------------------
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get the global LLM service instance."""

    global _llm_service

    if _llm_service is None:
        _llm_service = LLMService()

    return _llm_service