#!/usr/bin/env python3
"""
Simple LLM + AbletonMCP Integration Example
This script demonstrates how to connect an LLM to Ableton Live via LangChain and MCP tools.
"""

import os
from dotenv import load_dotenv
from langchain.agents import AgentType, create_react_agent, AgentExecutor
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from ableton_langchain_tool import get_ableton_tools

# Load environment variables
load_dotenv()

def main():
    """Main function demonstrating LLM + AbletonMCP integration."""
    
    # Check for Google API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_google_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        return
    
    print("🎵 LLM + Ableton Live Integration Example")
    print("=" * 50)
    
    # Initialize the LLM
    print("Initializing Google Gemini LLM...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Get Ableton tools
    print("Loading Ableton Live tools...")
    tools = get_ableton_tools()
    print(f"Loaded {len(tools)} Ableton Live tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Initialize the agent
    print("\nInitializing LangChain agent...")
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    print("\n" + "=" * 50)
    print("Agent ready! You can now ask questions about your Ableton Live session.")
    print("Example questions:")
    print("- 'What is the current session information?'")
    print("- 'Get information about track 0'")
    print("- 'Set the tempo to 120 BPM'")
    print("- 'Create a new MIDI track'")
    print("- 'Create a clip on track 0, slot 0'")
    print("- 'Add some notes to the clip'")
    print("\nType 'quit' to exit.")
    print("=" * 50)
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n🎵 Your request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 🎵")
                break
            
            if not user_input:
                continue
            
            print(f"\n🤖 Processing: {user_input}")
            print("-" * 30)
            
            # Run the agent
            response = agent_executor.invoke({"input": user_input})
            response = response["output"]
            
            print(f"\n✅ Response: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 🎵")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.")


def demo_session_info():
    """Demo function that automatically gets session info."""
    print("🎵 Demo: Getting Session Information")
    print("=" * 50)
    
    # Check for Google API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Get Ableton tools
    tools = get_ableton_tools()
    
    # Initialize the agent
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    # Ask for session info
    query = "What is the current session information in Ableton Live?"
    print(f"🤖 Query: {query}")
    print("-" * 30)
    
    try:
        response = agent_executor.invoke({"input": query})
        response = response["output"]
        print(f"\n✅ Response: {response}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run demo mode
        demo_session_info()
    else:
        # Run interactive mode
        main()
