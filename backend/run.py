# """
# AutoDocThinker - Agentic RAG System
# Main entry point for running the FastAPI application.
# """
# import os
# import uvicorn

# # Set USER_AGENT before any imports
# os.environ['USER_AGENT'] = 'AutoDocThinker/2.0'

# from app import app

# if __name__ == '__main__':
#     # Ensure directories exist
#     os.makedirs('uploads', exist_ok=True)
#     os.makedirs('vector_db', exist_ok=True)
    
#     # Get configuration
#     debug = os.environ.get('APP_ENV', 'development') == 'development'
#     port = int(os.environ.get('PORT', 5000))
    
#     # Run the application with uvicorn
#     uvicorn.run(
#         "app:app",
#         host="0.0.0.0",
#         port=port,
#         reload=Flase,
#         reload_dirs=["app"],
#         reload_excludes=["*.pyc", "__pycache__"]
#     )


"""
DocMind - Agentic RAG System
Main entry point for running the FastAPI application.
"""
import os
import uvicorn

# Set USER_AGENT before any imports
os.environ["USER_AGENT"] = "DocMind/2.0"

from app import app

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("vector_db", exist_ok=True)

    # Render provides PORT automatically
    port = int(os.environ.get("PORT", 10000))

    # Start FastAPI server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )