# LangChain Examples with Google Gemini

This repository contains simple examples demonstrating different LangChain capabilities using Google's Gemini AI model (free alternative to OpenAI).

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   
   Get your API key from: https://makersuite.google.com/app/apikey

## Examples

### 1. Basic LLM Example (`basic_example.py`)
Demonstrates a simple LLM call using LangChain with Google Gemini.

```bash
python basic_example.py
```

**What it does:**
- Initializes a ChatGoogleGenerativeAI model
- Sends a message and gets a response
- Shows basic LangChain usage with free Gemini API

### 2. Conversation with Memory (`conversation_example.py`)
Shows how to maintain conversation context using memory with Google Gemini.

```bash
python conversation_example.py
```

**What it does:**
- Creates a conversation chain with memory
- Maintains context across multiple messages
- Uses custom prompt templates
- Demonstrates conversation flow with Gemini

### 3. Document Q&A (`document_qa_example.py`)
Implements retrieval-augmented generation (RAG) for document-based question answering using Google Gemini.

```bash
python document_qa_example.py
```

**What it does:**
- Loads and chunks documents
- Creates vector embeddings using Google's embedding model
- Builds a vector store for retrieval
- Answers questions based on document content
- Shows RAG implementation with free Gemini API

## Key LangChain Concepts Demonstrated

- **LLMs**: Using Google's Gemini models (free alternative to OpenAI)
- **Memory**: ConversationBufferMemory for maintaining context
- **Chains**: ConversationChain and RetrievalQA chains
- **Prompts**: Custom prompt templates
- **Document Processing**: Text splitting and chunking
- **Vector Stores**: FAISS for similarity search
- **Embeddings**: Google's embedding models for text vectorization
- **Retrieval**: Document retrieval for augmented generation

## Requirements

- Python 3.8+
- Google API key (free from Google AI Studio)
- Internet connection for API calls

## MCP (Model Context Protocol) Examples

This repository also includes examples of using MCP tools to control Ableton Live:

### 4. Ableton MCP Examples

**Basic MCP Demo (`simple_ableton_demo.py`):**
```bash
python simple_ableton_demo.py
```

**Comprehensive MCP Guide (`ableton_mcp_example.py`):**
```bash
python ableton_mcp_example.py
```

**Workflow Examples (`ableton_workflow_example.py`):**
```bash
python ableton_workflow_example.py
```

**What MCP tools can do:**
- Create and manage MIDI tracks and clips
- Add MIDI notes and sequences
- Load instruments and effects
- Control device parameters
- Browse Ableton's content library
- Control playback and recording
- Set tempo and session parameters

**Setup Requirements:**
- Ableton Live 11 or 12
- MCP Remote Script for Ableton
- MCP Server running

## Next Steps

These examples provide a foundation for building more complex LangChain applications. You can extend them by:

- Adding more sophisticated memory types
- Implementing custom tools and agents
- Using different vector stores
- Adding more document loaders
- Creating custom chains and prompts
- **Integrating MCP tools with LangChain agents**

## Why Google Gemini?

- **Free to use** - No credit card required
- **Generous rate limits** - Much higher than OpenAI's free tier
- **High quality responses** - Comparable to GPT-3.5-turbo
- **Easy setup** - Just need a Google account
- **No quota issues** - Unlike OpenAI's paid plans
