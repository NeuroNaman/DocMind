"""
LLM Answer Agent - Generates answers using LLM.
Uses retrieved context to generate accurate responses.
"""

# from typing import Any, Dict

# from app.agents.base import BaseAgent
# from app.core.state import AgentState
# from app.services.llm_service import get_llm_service


# class LLMAnswerAgent(BaseAgent):
#     """
#     Generates answers using LLM based on retrieved context.
#     Produces human-like responses grounded in document content.
#     """

#     def execute(self, state: AgentState) -> Dict[str, Any]:
#         """
#         Generate answer based on context.

#         Args:
#             state: Current agent state

#         Returns:
#             State updates with generated answer
#         """
#         question = state.get("input", "")
#         context = state.get("context", [])
#         history = state.get("history", [])

#         if not question:
#             self.logger.warning("No question provided")
#             return {
#                 "answer": "No question was provided.",
#                 "source": "error",
#                 "next_agent": "executor_agent",
#             }

#         try:
#             llm_service = get_llm_service()

#             # Generate answer with context
#             if context:
#                 self.logger.info(
#                     f"Generating answer with {len(context)} context chunks"
#                 )

#                 # Use history if available
#                 if history:
#                     answer = llm_service.generate_with_history(
#                         question=question, context=context, history=history
#                     )
#                 else:
#                     answer = llm_service.generate_answer(
#                         question=question, context=context
#                     )

#                 source = "rag"
#             else:
#                 self.logger.warning("No context available, generating without context")
#                 answer = llm_service.generate_simple(
#                     f"Answer this question briefly: {question}"
#                 )
#                 source = "error"

#             self.logger.info("Answer generated successfully")

#             return {"answer": answer, "source": source, "next_agent": "executor_agent"}

#         except Exception as e:
#             self.logger.error(f"LLM generation failed: {e}")
#             return {
#                 "answer": f"Sorry, I encountered an error while generating the answer: {str(e)}",
#                 "source": "error",
#                 "next_agent": "executor_agent",
#             }


# # Standalone function for LangGraph compatibility
# def llm_answer_agent(state: AgentState) -> Dict[str, Any]:
#     """Standalone function wrapper for LangGraph."""
#     agent = LLMAnswerAgent()
#     return agent(state)








"""
LLM Answer Agent - Generates answers using LLM.
Uses retrieved context to generate accurate responses.
"""

# from typing import Any, Dict

# from app.agents.base import BaseAgent
# from app.core.state import AgentState
# from app.services.llm_service import get_llm_service


# class LLMAnswerAgent(BaseAgent):
#     """
#     Generates answers using LLM based on retrieved context.
#     Produces human-like responses grounded in document content.
#     """

#     def execute(self, state: AgentState) -> Dict[str, Any]:
#         """
#         Generate answer based on context.

#         Args:
#             state: Current agent state

#         Returns:
#             State updates with generated answer
#         """
#         question = state.get("input", "")
#         context = state.get("context", [])
#         history = state.get("history", [])

#         if not question:
#             self.logger.warning("No question provided")
#             return {
#                 "answer": "No question was provided.",
#                 "source": "error",
#                 "next_agent": "executor_agent",
#             }

#         try:
#             llm_service = get_llm_service()

#             # Generate answer with context
#             if context:
#                 self.logger.info(
#                     f"Generating answer with {len(context)} context chunks"
#                 )

#                 # Use history if available
#                 if history:
#                     answer = llm_service.generate_with_history(
#                         question=question, context=context, history=history
#                     )
#                 else:
#                     answer = llm_service.generate_answer(
#                         question=question, context=context
#                     )

#                 source = "rag"
#             else:
#                 self.logger.warning("No context available, generating without context")
#                 answer = llm_service.generate_simple(
#                     f"Answer this question briefly: {question}"
#                 )
#                 source = "error"

#             self.logger.info("Answer generated successfully")

#             return {"answer": answer, "source": source, "next_agent": "executor_agent"}

#         except Exception as e:
#             self.logger.error(f"LLM generation failed: {e}")
#             return {
#                 "answer": f"Sorry, I encountered an error while generating the answer: {str(e)}",
#                 "source": "error",
#                 "next_agent": "executor_agent",
#             }


# # Standalone function for LangGraph compatibility
# def llm_answer_agent(state: AgentState) -> Dict[str, Any]:
#     """Standalone function wrapper for LangGraph."""
#     agent = LLMAnswerAgent()
#     return agent(state)

"""
LLM Answer Agent - Generates answers using LLM with retrieved context.
"""

# from typing import Any, Dict

# from app.agents.base import BaseAgent
# from app.core.state import AgentState
# from app.services.llm_service import get_llm_service


# class LLMAnswerAgent(BaseAgent):
#     """
#     Generates answers using LLM based on retrieved context.
#     """

#     def execute(self, state: AgentState) -> Dict[str, Any]:

#         question = state.get("input", "")
#         context = state.get("context", [])
#         history = state.get("history", [])

#         if not question:
#             self.logger.warning("No question provided")

#             return {
#                 "answer": "No question was provided.",
#                 "source": "error",
#                 "next_agent": "executor_agent",
#             }

#         # IMPORTANT: If no context → fallback agent
#         if not context:

#             self.logger.info(
#                 "No context available -> routing to fallback agent"
#             )

#             return {
#                 "next_agent": "fallback_agent"
#             }

#         try:

#             llm_service = get_llm_service()

#             self.logger.info(
#                 f"Generating answer with {len(context)} context chunks"
#             )

#             # Use history if available
#             if history:
#                 answer = llm_service.generate_with_history(
#                     question=question,
#                     context=context,
#                     history=history,
#                 )
#             else:
#                 answer = llm_service.generate_answer(
#                     question=question,
#                     context=context,
#                 )

#             self.logger.info("Answer generated successfully")

#             return {
#                 "answer": answer,
#                 "source": "rag",
#                 "next_agent": "executor_agent",
#             }

#         except Exception as e:

#             self.logger.error(f"LLM generation failed: {e}")

#             return {
#                 "answer": "Error generating response.",
#                 "source": "error",
#                 "next_agent": "executor_agent",
#             }


# def llm_answer_agent(state: AgentState) -> Dict[str, Any]:
#     """LangGraph wrapper"""
#     agent = LLMAnswerAgent()
#     return agent(state)






from typing import Any, Dict

from app.agents.base import BaseAgent
from app.core.state import AgentState
from app.services.llm_service import get_llm_service


class LLMAnswerAgent(BaseAgent):
    """
    Generates answers using LLM based on retrieved context.
    If answer is not found in the document, routes to fallback agent.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:

        question = state.get("input", "")
        context = state.get("context", [])
        history = state.get("history", [])

        # ------------------------------------------------
        # No question
        # ------------------------------------------------
        if not question:
            self.logger.warning("No question provided")

            return {
                "answer": "No question was provided.",
                "source": "error",
                "next_agent": "executor_agent",
            }

        # ------------------------------------------------
        # No context → send to fallback
        # ------------------------------------------------
        if not context:

            self.logger.info(
                "No context available -> routing to fallback agent"
            )

            return {
                "next_agent": "fallback_agent"
            }

        try:

            llm_service = get_llm_service()

            self.logger.info(
                f"Generating answer with {len(context)} context chunks"
            )

            # ------------------------------------------------
            # Generate answer
            # ------------------------------------------------
            if history:
                answer = llm_service.generate_with_history(
                    question=question,
                    context=context,
                    history=history,
                )
            else:
                answer = llm_service.generate_answer(
                    question=question,
                    context=context,
                )

            # ------------------------------------------------
            # Detect if answer NOT in document
            # ------------------------------------------------
            answer_lower = answer.lower()

            negative_patterns = [
                "not contain",
                "not mentioned",
                "not present",
                "no information",
                "does not contain",
                "not found",
                "not provided in the context",
            ]

            if any(p in answer_lower for p in negative_patterns):

                self.logger.info(
                    "Answer not found in document -> routing to fallback agent"
                )

                return {
                    "context": [],
                    "next_agent": "fallback_agent"
                }

            # ------------------------------------------------
            # Valid RAG answer
            # ------------------------------------------------
            self.logger.info("Answer generated successfully")

            return {
                "answer": answer,
                "source": "rag",
                "next_agent": "executor_agent",
            }

        except Exception as e:

            self.logger.error(f"LLM generation failed: {e}")

            return {
                "answer": "Error generating response.",
                "source": "error",
                "next_agent": "executor_agent",
            }


# ------------------------------------------------
# LangGraph wrapper
# ------------------------------------------------
def llm_answer_agent(state: AgentState) -> Dict[str, Any]:
    """LangGraph wrapper"""
    agent = LLMAnswerAgent()
    return agent(state)