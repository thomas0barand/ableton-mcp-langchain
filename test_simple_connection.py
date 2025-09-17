#!/usr/bin/env python3
"""
Simple test script to verify AbletonMCP connection works
"""

from ableton_langchain_tool import get_ableton_tools

def test_connection():
    """Test basic connection to Ableton Live."""
    print("🎵 Testing Ableton Live Connection")
    print("=" * 40)
    
    # Get tools
    tools = get_ableton_tools()
    print(f"Loaded {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}")
    
    # Test session info
    print("\nTesting session info...")
    session_tool = next((t for t in tools if t.name == "get_session_info"), None)
    
    if session_tool:
        try:
            result = session_tool._run()
            print("✅ Connection successful!")
            print("Session info:", result)
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\nMake sure:")
            print("1. Ableton Live is running")
            print("2. The AbletonMCP remote script is installed and active")
            print("3. The MCP server is running")
    else:
        print("❌ Session info tool not found")

if __name__ == "__main__":
    test_connection()
