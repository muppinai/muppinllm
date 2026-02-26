"""
MuppinLLM - AI-Powered Crypto Market Analyst for Solana Tokens
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="muppinllm",
    version="1.0.0",
    author="Muppin Team",
    author_email="team@muppin.fun",
    description="AI-Powered Crypto Market Analyst for Solana Tokens - Bullish or Bearish Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muppin/muppinllm",
    project_urls={
        "Bug Tracker": "https://github.com/muppin/muppinllm/issues",
        "Documentation": "https://muppin.fun",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "emergentintegrations>=0.1.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "aiohttp>=3.9.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "black>=24.1.0",
            "isort>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "muppinllm=muppinllm.cli:main",
        ],
    },
    keywords="crypto solana ai llm market-analysis trading bullish bearish dex defi",
)
