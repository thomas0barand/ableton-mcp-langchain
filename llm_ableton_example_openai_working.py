#!/usr/bin/env python3
"""
Working LLM + Ableton Live Integration with OpenAI (Automatic Tool Selection)
This script uses LangChain's automatic tool selection to intelligently choose and execute tools.
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from ableton_langchain_tool import get_ableton_tools

# Load environment variables
load_dotenv()

def main():
    """Main function demonstrating LLM + AbletonMCP integration with OpenAI."""
    
    print("🎵 Working LLM + Ableton Live Integration (OpenAI with Auto Tool Selection)")
    print("=" * 70)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("\nGet your API key from: https://platform.openai.com/api-keys")
        print("OpenAI offers $5 free credit for new users!")
        return
    
    # Initialize the LLM
    print("Initializing OpenAI LLM...")
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Cheaper than GPT-4
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        print("✅ OpenAI LLM initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI: {e}")
        print("Make sure your API key is correct and you have credits available.")
        return
    
    # Get Ableton tools
    print("Loading Ableton Live tools...")
    tools = get_ableton_tools()
    print(f"Loaded {len(tools)} Ableton Live tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Prepare tools for function calling
    print("Preparing tools for automatic selection...")
    try:
        # Convert tools to function calling format
        functions = prepare_tools_for_llm(tools)
        print("✅ Tools prepared successfully!")
    except Exception as e:
        print(f"❌ Failed to prepare tools: {e}")
        return
    
    print("\n" + "=" * 70)
    print("Agent ready! You can now ask questions about your Ableton Live session.")
    print("The agent will automatically choose the right tools for your requests.")
    print("\nExample questions:")
    print("- 'What is the current session information?'")
    print("- 'Get information about track 0'")
    print("- 'Set the tempo to 120 BPM'")
    print("- 'Create a new MIDI track'")
    print("- 'Create a clip on track 0, slot 0'")
    print("- 'Add some notes to the clip'")
    print("\nType 'quit' to exit.")
    print("=" * 70)
    
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
            
            # Process request using automatic tool selection
            response = process_request_with_auto_tools(user_input, tools, llm, functions)
            
            print(f"\n✅ Response: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 🎵")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.")


def prepare_tools_for_llm(tools):
    """Convert LangChain tools to function calling format for OpenAI."""
    functions = []
    
    for tool in tools:
        # Create function schema for OpenAI function calling
        function_schema = {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
        
        # Add parameters based on tool's args_schema
        if hasattr(tool, 'args_schema') and tool.args_schema:
            schema_fields = tool.args_schema.model_fields
            for field_name, field_info in schema_fields.items():
                param_type = "string"
                if field_info.annotation == int:
                    param_type = "integer"
                elif field_info.annotation == float:
                    param_type = "number"
                elif field_info.annotation == bool:
                    param_type = "boolean"
                elif field_info.annotation == list:
                    param_type = "array"
                
                function_schema["parameters"]["properties"][field_name] = {
                    "type": param_type,
                    "description": field_info.description or f"Parameter {field_name}"
                }
                
                if field_info.default is None:  # Required parameter
                    function_schema["parameters"]["required"].append(field_name)
        
        functions.append(function_schema)
    
    return functions


def process_request_with_auto_tools(user_input, tools, llm, functions):
    """Process user request using automatic tool selection with function calling."""
    try:
        # Create a system message with available functions
        system_message = """You are a helpful assistant for Ableton Live music production. 
You have access to various tools to interact with Ableton Live sessions.

When a user asks about session information, tracks, tempo, or wants to create/modify content, 
use the appropriate tools to get the information or perform the actions.

Always provide clear, helpful responses based on the tool results. If you get JSON data from tools, 
explain it in a user-friendly way.

Available tools:
"""
        
        for tool in tools:
            system_message += f"- {tool.name}: {tool.description}\n"
        
        # Use function calling with the LLM
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
        
        # Call the LLM with function calling enabled
        response = llm.invoke(messages, functions=functions)
        
        # Check if the LLM wants to call a function
        if hasattr(response, 'additional_kwargs') and 'function_call' in response.additional_kwargs:
            function_call = response.additional_kwargs['function_call']
            function_name = function_call['name']
            function_args = json.loads(function_call['arguments'])
            
            # Find and execute the tool
            tool = next((t for t in tools if t.name == function_name), None)
            if tool:
                print(f"🔧 Executing tool: {function_name}")
                print(f"📝 Arguments: {function_args}")
                
                # Execute the tool with the arguments
                tool_result = tool._run(**function_args)
                print(f"📊 Tool result: {tool_result}")
                
                # Ask the LLM to analyze the result
                analysis_prompt = f"""The user asked: {user_input}

I executed the {function_name} tool with arguments {function_args} and got this result:
{tool_result}

Please provide a clear, helpful response based on this result. If the result contains JSON data, explain it in a user-friendly way."""
                
                analysis_response = llm.invoke([
                    {"role": "system", "content": "You are a helpful assistant that explains tool results in a user-friendly way."},
                    {"role": "user", "content": analysis_prompt}
                ])
                
                return analysis_response.content
            else:
                return f"Error: Tool '{function_name}' not found."
        else:
            # No function call needed, return the response directly
            return response.content
            
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def process_request_with_llm(user_input, tools, llm):
    """Process user request using tools and LLM."""
    
    # First, try to use tools directly based on keywords
    tool_response = process_request_with_tools(user_input, tools)
    
    if tool_response and not tool_response.startswith("I didn't understand"):
        # Tool was executed successfully, now use LLM to analyze the result
        try:
            # Create a context about what happened
            tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
            
            prompt = f"""You are a helpful assistant for Ableton Live music production. 

Available tools:
{tool_descriptions}

User request: {user_input}

Tool execution result: {tool_response}

Please analyze the tool execution result and provide a clear, helpful summary of what was found or accomplished. 
If the result contains JSON data, parse it and explain it in a user-friendly way.
If the result indicates an error, explain what went wrong and suggest alternatives.
"""
            
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Tool executed successfully: {tool_response}\n\nError analyzing result: {str(e)}"
    
    # If no tool matched, use LLM to generate a response
    try:
        # Create a context about available tools
        tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
        
        prompt = f"""You are a helpful assistant for Ableton Live music production. 
        
Available tools:
{tool_descriptions}

User request: {user_input}

Please provide a helpful response about Ableton Live or suggest which tool might be useful for this request.
If the user wants to control Ableton Live, suggest using one of the available tools.
"""
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Sorry, I couldn't process that request. Error: {str(e)}"


def process_request_with_tools(user_input, tools):
    """Process user request using available tools."""
    
    # Simple keyword-based tool selection
    user_lower = user_input.lower()
    
    if ("session" in user_lower and ("info" in user_lower or "information" in user_lower)) or \
       ("current" in user_lower and "session" in user_lower) or \
       ("what" in user_lower and "session" in user_lower):
        # Get session info
        tool = next((t for t in tools if t.name == "get_session_info"), None)
        if tool:
            try:
                return tool._run()
            except Exception as e:
                return f"Error getting session info: {str(e)}"
    
    elif "track" in user_lower and "info" in user_lower:
        # Get track info - extract track number
        track_num = 0
        words = user_input.split()
        for i, word in enumerate(words):
            if word.isdigit():
                track_num = int(word)
                break
        
        tool = next((t for t in tools if t.name == "get_track_info"), None)
        if tool:
            return tool._run(track_num)
    
    elif "tempo" in user_lower:
        # Set tempo - extract tempo value
        tempo = 120
        words = user_input.split()
        for i, word in enumerate(words):
            if word.isdigit():
                tempo = int(word)
                break
        
        tool = next((t for t in tools if t.name == "set_tempo"), None)
        if tool:
            return tool._run(tempo)
    
    elif "create" in user_lower and "track" in user_lower:
        # Create MIDI track
        tool = next((t for t in tools if t.name == "create_midi_track"), None)
        if tool:
            return tool._run()
    
    elif "create" in user_lower and "clip" in user_lower:
        # Create clip - extract track and clip numbers
        track_num = 0
        clip_num = 0
        words = user_input.split()
        for i, word in enumerate(words):
            if word.isdigit():
                if track_num == 0:
                    track_num = int(word)
                else:
                    clip_num = int(word)
                    break
        
        tool = next((t for t in tools if t.name == "create_clip"), None)
        if tool:
            return tool._run(track_num, clip_num)
    
    elif "add" in user_lower and "notes" in user_lower:
        # Add notes - extract track and clip numbers
        track_num = 0
        clip_num = 0
        words = user_input.split()
        for i, word in enumerate(words):
            if word.isdigit():
                if track_num == 0:
                    track_num = int(word)
                else:
                    clip_num = int(word)
                    break
        
        # Create some example notes
        notes = [
            {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
            {"pitch": 64, "start_time": 1.0, "duration": 0.5, "velocity": 100},
            {"pitch": 67, "start_time": 2.0, "duration": 0.5, "velocity": 100},
        ]
        
        tool = next((t for t in tools if t.name == "add_notes_to_clip"), None)
        if tool:
            return tool._run(track_num, clip_num, notes)
    
    elif "fire" in user_lower or "play" in user_lower:
        # Fire clip - extract track and clip numbers
        track_num = 0
        clip_num = 0
        words = user_input.split()
        for i, word in enumerate(words):
            if word.isdigit():
                if track_num == 0:
                    track_num = int(word)
                else:
                    clip_num = int(word)
                    break
        
        tool = next((t for t in tools if t.name == "fire_clip"), None)
        if tool:
            return tool._run(track_num, clip_num)
    
    return "I didn't understand that request. Please try again."


def demo_session_info():
    """Demo function that automatically gets session info using the agent."""
    print("🎵 Demo: Getting Session Information (OpenAI with Auto Tool Selection)")
    print("=" * 70)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return
    
    # Initialize the LLM
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        print("✅ OpenAI LLM initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI: {e}")
        return
    
    # Get Ableton tools and prepare for function calling
    tools = get_ableton_tools()
    try:
        functions = prepare_tools_for_llm(tools)
        print("✅ Tools prepared successfully!")
    except Exception as e:
        print(f"❌ Failed to prepare tools: {e}")
        return
    
    # Ask for session info
    query = "What is the current session information in Ableton Live?"
    print(f"🤖 Query: {query}")
    print("-" * 30)
    
    try:
        response = process_request_with_auto_tools(query, tools, llm, functions)
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

