# """
# LangGraph workflow definition.
# Defines the main agentic workflow graph.
# """

# from typing import Tuple

# from langgraph.graph import END, StateGraph

# from app.agents.executor import executor_agent
# from app.agents.fallback import fallback_agent
# from app.agents.ingestion import ingestion_agent
# from app.agents.llm_answer import llm_answer_agent
# from app.agents.planner import planner_agent
# from app.agents.retriever import retriever_agent
# from app.agents.tool_router import tool_router_agent
# from app.core.state import AgentState
# from app.utils.logger import get_logger
# from app.workflow.edges import route_after_planner

# logger = get_logger("workflow")

# # Global compiled workflow
# _workflow = None


# def create_workflow() -> StateGraph:
#     """
#     Create the LangGraph workflow.

#     Returns:
#         Compiled workflow graph
#     """
#     logger.info("Creating workflow graph...")

#     # Initialize the graph with state schema
#     workflow = StateGraph(AgentState)

#     # Add all agent nodes
#     workflow.add_node("tool_router_agent", tool_router_agent)
#     workflow.add_node("ingestion_agent", ingestion_agent)
#     workflow.add_node("planner_agent", planner_agent)
#     workflow.add_node("retriever_agent", retriever_agent)
#     workflow.add_node("llm_answer_agent", llm_answer_agent)
#     workflow.add_node("fallback_agent", fallback_agent)
#     workflow.add_node("executor_agent", executor_agent)

#     # Set entry point
#     workflow.set_entry_point("tool_router_agent")

#     # Define edges
#     # Tool router -> Ingestion (always, ingestion decides whether to process)
#     workflow.add_edge("tool_router_agent", "ingestion_agent")

#     # Ingestion -> Planner
#     workflow.add_edge("ingestion_agent", "planner_agent")

#     # Planner -> (Retriever or Fallback) based on document availability
#     workflow.add_conditional_edges(
#         "planner_agent",
#         route_after_planner,
#         {"retriever_agent": "retriever_agent", "fallback_agent": "fallback_agent"},
#     )

#     # Retriever -> LLM Answer
#     workflow.add_edge("retriever_agent", "llm_answer_agent")

#     # LLM Answer -> Executor
#     workflow.add_edge("llm_answer_agent", "executor_agent")

#     # Fallback -> Executor
#     workflow.add_edge("fallback_agent", "executor_agent")

#     # Executor -> END
#     workflow.add_edge("executor_agent", END)

#     # Compile the workflow
#     compiled = workflow.compile()
#     logger.info("Workflow graph created and compiled successfully")

#     return compiled


# def get_workflow():
#     """
#     Get the global workflow instance (singleton).

#     Returns:
#         Compiled workflow
#     """
#     global _workflow
#     if _workflow is None:
#         _workflow = create_workflow()
#     return _workflow


# def process_query(
#     input_text: str, file_path: str = None, file_type: str = None
# ) -> Tuple[str, str]:
#     """
#     Process a query through the workflow.

#     Args:
#         input_text: User's query
#         file_path: Path to file or URL (optional)
#         file_type: Type of file (pdf, docx, txt, url)

#     Returns:
#         Tuple of (answer, source)
#     """
#     logger.info(f"Processing query: {input_text[:50]}...")

#     # Prepare initial state
#     initial_state: AgentState = {
#         "input": input_text,
#         "file_content": file_path,
#         "file_type": file_type,
#         "context": None,
#         "answer": None,
#         "history": [],
#         "source": None,
#         "error": None,
#         "metadata": None,
#     }

#     try:
#         # Get workflow and invoke
#         workflow = get_workflow()
#         result = workflow.invoke(initial_state)

#         # Extract results
#         answer = result.get("answer", "No answer generated")
#         source = result.get("source", "unknown")

#         # Check for errors
#         if result.get("error"):
#             logger.warning(f"Workflow completed with error: {result['error']}")

#         logger.info(f"Query processed successfully (source: {source})")
#         return answer, source

#     except Exception as e:
#         logger.error(f"Workflow execution failed: {e}")
#         return f"Sorry, an error occurred: {str(e)}", "error"


# def reset_workflow():
#     """Reset the global workflow instance."""
#     global _workflow
#     _workflow = None
#     logger.info("Workflow reset")


"""
LangGraph workflow definition.
Defines the main agentic workflow graph.
"""

# from typing import Tuple

# from langgraph.graph import END, StateGraph

# from app.agents.executor import executor_agent
# from app.agents.fallback import fallback_agent
# from app.agents.ingestion import ingestion_agent
# from app.agents.llm_answer import llm_answer_agent
# from app.agents.planner import planner_agent
# from app.agents.retriever import retriever_agent
# from app.agents.tool_router import tool_router_agent
# from app.core.state import AgentState
# from app.utils.logger import get_logger
# from app.workflow.edges import route_after_planner

# logger = get_logger("workflow")

# # Global compiled workflow
# _workflow = None


# def route_after_retriever(state: AgentState) -> str:
#     """
#     Decide next step after retriever.
#     """
#     if state.get("context"):
#         return "llm_answer_agent"
#     return "fallback_agent"


# def create_workflow() -> StateGraph:
#     """
#     Create the LangGraph workflow.

#     Returns:
#         Compiled workflow graph
#     """
#     logger.info("Creating workflow graph...")

#     workflow = StateGraph(AgentState)

#     # ----------------------------
#     # Add agent nodes
#     # ----------------------------
#     workflow.add_node("tool_router_agent", tool_router_agent)
#     workflow.add_node("ingestion_agent", ingestion_agent)
#     workflow.add_node("planner_agent", planner_agent)
#     workflow.add_node("retriever_agent", retriever_agent)
#     workflow.add_node("llm_answer_agent", llm_answer_agent)
#     workflow.add_node("fallback_agent", fallback_agent)
#     workflow.add_node("executor_agent", executor_agent)

#     # ----------------------------
#     # Entry point
#     # ----------------------------
#     workflow.set_entry_point("tool_router_agent")

#     # ----------------------------
#     # Tool Router → Ingestion
#     # ----------------------------
#     workflow.add_edge("tool_router_agent", "ingestion_agent")

#     # ----------------------------
#     # Ingestion → Planner
#     # ----------------------------
#     workflow.add_edge("ingestion_agent", "planner_agent")

#     # ----------------------------
#     # Planner → Retriever OR Fallback
#     # ----------------------------
#     workflow.add_conditional_edges(
#         "planner_agent",
#         route_after_planner,
#         {
#             "retriever_agent": "retriever_agent",
#             "fallback_agent": "fallback_agent",
#         },
#     )

#     # ----------------------------
#     # Retriever → LLM OR Fallback
#     # ----------------------------
#     workflow.add_conditional_edges(
#         "retriever_agent",
#         route_after_retriever,
#         {
#             "llm_answer_agent": "llm_answer_agent",
#             "fallback_agent": "fallback_agent",
#         },
#     )

#     # ----------------------------
#     # LLM → Executor
#     # ----------------------------
#     workflow.add_edge("llm_answer_agent", "executor_agent")

#     # ----------------------------
#     # Fallback → Executor
#     # ----------------------------
#     workflow.add_edge("fallback_agent", "executor_agent")

#     # ----------------------------
#     # Executor → END
#     # ----------------------------
#     workflow.add_edge("executor_agent", END)

#     compiled = workflow.compile()

#     logger.info("Workflow graph created and compiled successfully")

#     return compiled


# def get_workflow():
#     """
#     Get the global workflow instance (singleton).
#     """
#     global _workflow

#     if _workflow is None:
#         _workflow = create_workflow()

#     return _workflow


# def process_query(
#     input_text: str, file_path: str = None, file_type: str = None
# ) -> Tuple[str, str]:
#     """
#     Process a query through the workflow.
#     """

#     logger.info(f"Processing query: {input_text[:50]}...")

#     initial_state: AgentState = {
#         "input": input_text,
#         "file_content": file_path,
#         "file_type": file_type,
#         "context": None,
#         "answer": None,
#         "history": [],
#         "source": None,
#         "error": None,
#         "metadata": None,
#     }

#     try:
#         workflow = get_workflow()

#         result = workflow.invoke(initial_state)

#         answer = result.get("answer", "No answer generated")
#         source = result.get("source", "unknown")

#         if result.get("error"):
#             logger.warning(f"Workflow completed with error: {result['error']}")

#         logger.info(f"Query processed successfully (source: {source})")

#         return answer, source

#     except Exception as e:
#         logger.error(f"Workflow execution failed: {e}")

#         return f"Sorry, an error occurred: {str(e)}", "error"


# def reset_workflow():
#     """
#     Reset the global workflow instance.
#     """
#     global _workflow
#     _workflow = None
#     logger.info("Workflow reset")

# from typing import Tuple

# from langgraph.graph import END, StateGraph

# from app.agents.executor import executor_agent
# from app.agents.fallback import fallback_agent
# from app.agents.ingestion import ingestion_agent
# from app.agents.llm_answer import llm_answer_agent
# from app.agents.planner import planner_agent
# from app.agents.retriever import retriever_agent
# from app.agents.tool_router import tool_router_agent
# from app.core.state import AgentState
# from app.utils.logger import get_logger
# from app.workflow.edges import route_after_planner

# logger = get_logger("workflow")

# # Global compiled workflow
# _workflow = None


# def route_after_retriever(state: AgentState) -> str:
#     """
#     Decide next step after retriever.

#     Logic:
#     1. If retriever explicitly set next_agent → respect it
#     2. If no context → fallback
#     3. If similarity score is weak → fallback
#     4. Otherwise → LLM answer agent
#     """

#     # Respect retriever explicit routing
#     next_agent = state.get("next_agent")
#     if next_agent:
#         return next_agent

#     context = state.get("context")
#     metadata = state.get("metadata") or {}

#     # If no retrieved chunks
#     if not context or len(context) == 0:
#         return "fallback_agent"

#     # Check similarity quality
#     avg_score = metadata.get("avg_score")

#     if avg_score is not None:
#         # Chroma cosine distance:
#         # lower = better match
#         # >1.6 usually irrelevant
#         if avg_score > 1.6:
#             logger.info(
#                 f"Retriever score too weak ({avg_score}) → routing to fallback"
#             )
#             return "fallback_agent"

#     return "llm_answer_agent"


# def create_workflow() -> StateGraph:
#     """
#     Create the LangGraph workflow.
#     """

#     logger.info("Creating workflow graph...")

#     workflow = StateGraph(AgentState)

#     # ------------------------------------------------
#     # Register agents
#     # ------------------------------------------------
#     workflow.add_node("tool_router_agent", tool_router_agent)
#     workflow.add_node("ingestion_agent", ingestion_agent)
#     workflow.add_node("planner_agent", planner_agent)
#     workflow.add_node("retriever_agent", retriever_agent)
#     workflow.add_node("llm_answer_agent", llm_answer_agent)
#     workflow.add_node("fallback_agent", fallback_agent)
#     workflow.add_node("executor_agent", executor_agent)

#     # ------------------------------------------------
#     # Entry point
#     # ------------------------------------------------
#     workflow.set_entry_point("tool_router_agent")

#     # ------------------------------------------------
#     # Tool Router → Ingestion
#     # ------------------------------------------------
#     workflow.add_edge(
#         "tool_router_agent",
#         "ingestion_agent",
#     )

#     # ------------------------------------------------
#     # Ingestion → Planner
#     # ------------------------------------------------
#     workflow.add_edge(
#         "ingestion_agent",
#         "planner_agent",
#     )

#     # ------------------------------------------------
#     # Planner → Retriever OR Fallback
#     # ------------------------------------------------
#     workflow.add_conditional_edges(
#         "planner_agent",
#         route_after_planner,
#         {
#             "retriever_agent": "retriever_agent",
#             "fallback_agent": "fallback_agent",
#         },
#     )

#     # ------------------------------------------------
#     # Retriever → LLM OR Fallback
#     # ------------------------------------------------
#     workflow.add_conditional_edges(
#         "retriever_agent",
#         route_after_retriever,
#         {
#             "llm_answer_agent": "llm_answer_agent",
#             "fallback_agent": "fallback_agent",
#         },
#     )

#     # ------------------------------------------------
#     # LLM → Executor
#     # ------------------------------------------------
#     workflow.add_edge(
#         "llm_answer_agent",
#         "executor_agent",
#     )

#     # ------------------------------------------------
#     # Fallback → Executor
#     # ------------------------------------------------
#     workflow.add_edge(
#         "fallback_agent",
#         "executor_agent",
#     )

#     # ------------------------------------------------
#     # Executor → END
#     # ------------------------------------------------
#     workflow.add_edge(
#         "executor_agent",
#         END,
#     )

#     compiled = workflow.compile()

#     logger.info("Workflow graph created and compiled successfully")

#     return compiled


# def get_workflow():
#     """
#     Get the global workflow instance (singleton).
#     """

#     global _workflow

#     if _workflow is None:
#         _workflow = create_workflow()

#     return _workflow


# def process_query(
#     input_text: str,
#     file_path: str = None,
#     file_type: str = None,
# ) -> Tuple[str, str]:
#     """
#     Process a query through the workflow.
#     """

#     logger.info(f"Processing query: {input_text[:50]}...")

#     initial_state: AgentState = {
#         "input": input_text,
#         "file_content": file_path,
#         "file_type": file_type,
#         "context": None,
#         "answer": None,
#         "history": [],
#         "source": None,
#         "error": None,
#         "metadata": None,
#     }

#     try:
#         workflow = get_workflow()

#         result = workflow.invoke(initial_state)

#         answer = result.get("answer", "No answer generated")
#         source = result.get("source", "unknown")

#         if result.get("error"):
#             logger.warning(f"Workflow completed with error: {result['error']}")

#         logger.info(f"Query processed successfully (source: {source})")

#         return answer, source

#     except Exception as e:

#         logger.error(f"Workflow execution failed: {e}")

#         return f"Sorry, an error occurred: {str(e)}", "error"


# def reset_workflow():
#     """
#     Reset the global workflow instance.
#     """

#     global _workflow

#     _workflow = None

#     logger.info("Workflow reset")




# from typing import Tuple

# from langgraph.graph import END, StateGraph

# from app.agents.executor import executor_agent
# from app.agents.fallback import fallback_agent
# from app.agents.ingestion import ingestion_agent
# from app.agents.llm_answer import llm_answer_agent
# from app.agents.planner import planner_agent
# from app.agents.retriever import retriever_agent
# from app.agents.tool_router import tool_router_agent
# from app.core.state import AgentState
# from app.utils.logger import get_logger
# from app.workflow.edges import route_after_planner

# logger = get_logger("workflow")

# # Global compiled workflow
# _workflow = None


# def route_after_retriever(state: AgentState) -> str:
#     """
#     Decide next step after retriever.
#     """

#     # Respect retriever routing
#     next_agent = state.get("next_agent")
#     if next_agent:
#         return next_agent

#     context = state.get("context")
#     metadata = state.get("metadata") or {}

#     # No retrieved chunks
#     if not context or len(context) == 0:
#         logger.info("No context retrieved -> fallback")
#         return "fallback_agent"

#     # Check similarity score
#     avg_score = metadata.get("avg_score")

#     if avg_score is not None:
#         if avg_score > 1.6:
#             logger.info(
#                 f"Retriever score weak ({avg_score}) -> routing to fallback"
#             )
#             return "fallback_agent"

#     return "llm_answer_agent"


# def create_workflow() -> StateGraph:
#     """
#     Create LangGraph workflow.
#     """

#     logger.info("Creating workflow graph...")

#     workflow = StateGraph(AgentState)

#     # ------------------------------------------------
#     # Register agents
#     # ------------------------------------------------
#     workflow.add_node("tool_router_agent", tool_router_agent)
#     workflow.add_node("ingestion_agent", ingestion_agent)
#     workflow.add_node("planner_agent", planner_agent)
#     workflow.add_node("retriever_agent", retriever_agent)
#     workflow.add_node("llm_answer_agent", llm_answer_agent)
#     workflow.add_node("fallback_agent", fallback_agent)
#     workflow.add_node("executor_agent", executor_agent)

#     # ------------------------------------------------
#     # Entry point
#     # ------------------------------------------------
#     workflow.set_entry_point("tool_router_agent")

#     # ------------------------------------------------
#     # Router → Ingestion
#     # ------------------------------------------------
#     workflow.add_edge("tool_router_agent", "ingestion_agent")

#     # ------------------------------------------------
#     # Ingestion → Planner
#     # ------------------------------------------------
#     workflow.add_edge("ingestion_agent", "planner_agent")

#     # ------------------------------------------------
#     # Planner → Retriever OR Fallback
#     # ------------------------------------------------
#     workflow.add_conditional_edges(
#         "planner_agent",
#         route_after_planner,
#         {
#             "retriever_agent": "retriever_agent",
#             "fallback_agent": "fallback_agent",
#         },
#     )

#     # ------------------------------------------------
#     # Retriever → LLM OR Fallback
#     # ------------------------------------------------
#     workflow.add_conditional_edges(
#         "retriever_agent",
#         route_after_retriever,
#         {
#             "llm_answer_agent": "llm_answer_agent",
#             "fallback_agent": "fallback_agent",
#         },
#     )

#     # ------------------------------------------------
#     # LLM → Executor
#     # ------------------------------------------------
#     workflow.add_edge("llm_answer_agent", "executor_agent")

#     # ------------------------------------------------
#     # Fallback → Executor
#     # ------------------------------------------------
#     workflow.add_edge("fallback_agent", "executor_agent")

#     # ------------------------------------------------
#     # Executor → END
#     # ------------------------------------------------
#     workflow.add_edge("executor_agent", END)

#     compiled = workflow.compile()

#     logger.info("Workflow graph created successfully")

#     return compiled


# def get_workflow():
#     """
#     Get global workflow instance.
#     """

#     global _workflow

#     if _workflow is None:
#         _workflow = create_workflow()

#     return _workflow


# def process_query(
#     input_text: str,
#     file_path: str = None,
#     file_type: str = None,
# ) -> Tuple[str, str]:
#     """
#     Process user query through workflow.
#     """

#     logger.info(f"Processing query: {input_text[:50]}...")

#     # ------------------------------------------------
#     # FIX: Skip QA pipeline during document upload
#     # ------------------------------------------------
#     if input_text.lower().startswith("initialize"):
#         logger.info("Document initialization detected - skipping QA pipeline")
#         return "Document processed successfully.", "system"

#     initial_state: AgentState = {
#         "input": input_text,
#         "file_content": file_path,
#         "file_type": file_type,
#         "context": None,
#         "answer": None,
#         "history": [],
#         "source": None,
#         "error": None,
#         "metadata": None,
#     }

#     try:

#         workflow = get_workflow()

#         result = workflow.invoke(initial_state)

#         answer = result.get("answer", "No answer generated")
#         source = result.get("source", "unknown")

#         if result.get("error"):
#             logger.warning(f"Workflow error: {result['error']}")

#         logger.info(f"Query processed successfully (source: {source})")

#         return answer, source

#     except Exception as e:

#         logger.error(f"Workflow execution failed: {e}")

#         return f"Sorry, an error occurred: {str(e)}", "error"


# def reset_workflow():
#     """
#     Reset global workflow instance.
#     """

#     global _workflow

#     _workflow = None

#     logger.info("Workflow reset")







from typing import Tuple

from langgraph.graph import END, StateGraph

from app.agents.executor import executor_agent
from app.agents.fallback import fallback_agent
from app.agents.ingestion import ingestion_agent
from app.agents.llm_answer import llm_answer_agent
from app.agents.planner import planner_agent
from app.agents.retriever import retriever_agent
from app.agents.tool_router import tool_router_agent
from app.core.state import AgentState
from app.utils.logger import get_logger
from app.workflow.edges import route_after_planner

logger = get_logger("workflow")

# Global compiled workflow
_workflow = None


# ------------------------------------------------
# Retriever Routing
# ------------------------------------------------
def route_after_retriever(state: AgentState) -> str:

    next_agent = state.get("next_agent")
    if next_agent:
        return next_agent

    context = state.get("context")
    metadata = state.get("metadata") or {}

    if not context or len(context) == 0:
        logger.info("Retriever found no context -> fallback")
        return "fallback_agent"

    avg_score = metadata.get("avg_score")

    if avg_score is not None and avg_score > 1.6:
        logger.info(f"Retriever similarity weak ({avg_score}) -> fallback")
        return "fallback_agent"

    return "llm_answer_agent"


# ------------------------------------------------
# LLM Routing (VERY IMPORTANT FIX)
# ------------------------------------------------
def route_after_llm(state: AgentState) -> str:

    next_agent = state.get("next_agent")

    if next_agent == "fallback_agent":
        logger.info("LLM indicated fallback required")
        return "fallback_agent"

    return "executor_agent"


# ------------------------------------------------
# Create Workflow
# ------------------------------------------------
def create_workflow() -> StateGraph:

    logger.info("Creating workflow graph...")

    workflow = StateGraph(AgentState)

    # Register agents
    workflow.add_node("tool_router_agent", tool_router_agent)
    workflow.add_node("ingestion_agent", ingestion_agent)
    workflow.add_node("planner_agent", planner_agent)
    workflow.add_node("retriever_agent", retriever_agent)
    workflow.add_node("llm_answer_agent", llm_answer_agent)
    workflow.add_node("fallback_agent", fallback_agent)
    workflow.add_node("executor_agent", executor_agent)

    # Entry point
    workflow.set_entry_point("tool_router_agent")

    # Router → Ingestion
    workflow.add_edge("tool_router_agent", "ingestion_agent")

    # Ingestion → Planner
    workflow.add_edge("ingestion_agent", "planner_agent")

    # Planner → Retriever OR Fallback
    workflow.add_conditional_edges(
        "planner_agent",
        route_after_planner,
        {
            "retriever_agent": "retriever_agent",
            "fallback_agent": "fallback_agent",
        },
    )

    # Retriever → LLM OR Fallback
    workflow.add_conditional_edges(
        "retriever_agent",
        route_after_retriever,
        {
            "llm_answer_agent": "llm_answer_agent",
            "fallback_agent": "fallback_agent",
        },
    )

    # LLM → Executor OR Fallback
    workflow.add_conditional_edges(
        "llm_answer_agent",
        route_after_llm,
        {
            "fallback_agent": "fallback_agent",
            "executor_agent": "executor_agent",
        },
    )

    # Fallback → Executor
    workflow.add_edge("fallback_agent", "executor_agent")

    # Executor → END
    workflow.add_edge("executor_agent", END)

    compiled = workflow.compile()

    logger.info("Workflow graph created successfully")

    return compiled


# ------------------------------------------------
# Get Workflow Singleton
# ------------------------------------------------
def get_workflow():

    global _workflow

    if _workflow is None:
        _workflow = create_workflow()

    return _workflow


# ------------------------------------------------
# Process Query
# ------------------------------------------------
def process_query(
    input_text: str,
    file_path: str = None,
    file_type: str = None,
) -> Tuple[str, str]:

    logger.info(f"Processing query: {input_text[:50]}...")

    # Skip QA pipeline during upload
    if input_text.lower().startswith("initialize"):
        logger.info("Document initialization detected - skipping QA pipeline")
        return "Document processed successfully.", "system"

    initial_state: AgentState = {
        "input": input_text,
        "file_content": file_path,
        "file_type": file_type,
        "context": None,
        "answer": None,
        "history": [],
        "source": None,
        "error": None,
        "metadata": None,
    }

    try:

        workflow = get_workflow()

        result = workflow.invoke(initial_state)

        answer = result.get("answer", "No answer generated")
        source = result.get("source", "unknown")

        if result.get("error"):
            logger.warning(f"Workflow error: {result['error']}")

        logger.info(f"Query processed successfully (source: {source})")

        return answer, source

    except Exception as e:

        logger.error(f"Workflow execution failed: {e}")

        return f"Sorry, an error occurred: {str(e)}", "error"


# ------------------------------------------------
# Reset Workflow
# ------------------------------------------------
def reset_workflow():

    global _workflow

    _workflow = None

    logger.info("Workflow reset")