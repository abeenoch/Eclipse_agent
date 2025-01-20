# Eclipse AI Agent

An industry-grade AI assistant specialized in providing technical support and code samples for Eclipse (L2 layer solutions), leveraging advanced AI models and web tools.

![AI Assistant](https://img.shields.io/badge/AI-Assistant-blueviolet)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Workflows](https://img.shields.io/badge/Storage-SQLite-success)

## Overview

The Eclipse AI Agent is a sophisticated workflow-driven assistant that combines:
- GPT-4o's reasoning capabilities
- Tavily search integration
- Web scraping functionality
- Persistent conversation history
- SQLite-based caching system

Designed specifically for Eclipse L2 layer development support, providing contextual responses with relevant code examples.

## Features

- **Intelligent Query Processing**: Multi-stage analysis of technical queries
- **Web Integration**: 
  - Tavily API for optimized search
  - Crawl4AI for dynamic content scraping
- **Conversation Continuity**: Context-aware interactions using history tracking
- **Performance Optimization**:
  - SQLite-based response caching
  - Automatic session management
- **Developer Focus**:
  - Markdown-formatted responses
  - Tool call visibility
  - Built-in monitoring

## Installation

```bash
git clone [your-repository-url]
cd eclipse-ai-agent
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
