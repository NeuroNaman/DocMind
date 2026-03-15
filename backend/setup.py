from setuptools import setup, find_packages

setup(
    name="AutoDocThinker",
    version="1.0.0",
    description="An AI-powered Intelligent Search Engine with Reasoning + Tool Usage Logic.",
    author="Md Emon Hasan",
    author_email="iconicemon01@gmail.com",
    url="https://github.com/Md-Emon-Hasan/AutoDocThinker",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        'streamlit',
        'langchain',
        'chromadb',
        'sentence-transformers',
        "langgraph",
        "langchain-core",
        "langchain-groq",
        "langchain-community",
        "huggingface-hub"
        
        # Document processing dependencies
        'docx2txt',
        'unstructured[pdf,image]',
        'pdf2image',
        'pytesseract',
        'Pillow',
        'duckduckgo-search',
        'yfinance',
        'transformers',
        "unstructured",
        "pypdf",
        "python-docx",
        "html5lib",
        "tqdm",
        "pymupdf",
        "newspaper3k",
        "werkzeug",
        "marked",
        "sentence-transformers",
        "transformers",
        "torch",
        "chromadb",
        "typing-extensions",
        "huggingface-hub",
        
        # Utility and support dependencies
        'beautifulsoup4',
        'html2text',
        'pdfminer.six',
        'requests',
        'python-dotenv',  
        'setuptools'
    ],
    extras_require={
        'dev': [
            'pytest',  
            'black',  
            'flake8',
            'pre-commit'
        ],
        'deploy': [
            'docker', 
            'fastapi', 
            'gunicorn',
        ]
    },
    python_requires='>=3.7', 
    entry_points={
        'console_scripts': [
            'ai-doc-qa=your_module.app:run', 
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
