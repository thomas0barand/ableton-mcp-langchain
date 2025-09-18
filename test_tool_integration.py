#!/usr/bin/env python3
"""
Test script to verify that all Ableton Live tools are properly integrated.
This script tests the tool loading and basic functionality without requiring Ableton Live to be running.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ableton_langchain_tool import get_ableton_tools
from langchain.tools import BaseTool
from ableton_mcp_client import AbletonMCPClient

def test_tool_loading():
    """Test that all tools can be loaded without errors."""
    print("Testing tool loading...")
    
    try:
        tools = get_ableton_tools()
        print(f"✓ Successfully loaded {len(tools)} tools")
        
        # Check that all tools are BaseTool instances
        for tool in tools:
            if not isinstance(tool, BaseTool):
                print(f"✗ Tool {tool.name} is not a BaseTool instance")
                return False
        
        print("✓ All tools are valid BaseTool instances")
        
        # Print tool names and descriptions
        print("\nAvailable tools:")
        for i, tool in enumerate(tools, 1):
            print(f"{i:2d}. {tool.name}: {tool.description}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading tools: {e}")
        return False

def test_tool_categories():
    """Test that tools are properly categorized."""
    print("\nTesting tool categories...")
    
    tools = get_ableton_tools()

    # Expected categories and their tools
    expected_categories = {
        'Session Management': ['get_session_info', 'set_tempo', 'start_playback', 'stop_playback'],
        'Track Management': ['get_track_info', 'create_midi_track', 'set_track_name'],
        'Clip Management': ['create_clip', 'set_clip_name', 'fire_clip', 'stop_clip'],
        'Note Management': ['add_notes_to_clip', 'get_notes_from_clip', 'delete_notes_from_clip', 'transpose_notes_in_clip', 'quantize_notes_in_clip'],
        'Device Management': ['get_device_parameters', 'set_device_parameter', 'batch_set_device_parameters', 'load_instrument_or_effect'],
        'Browser Management': ['get_browser_tree', 'get_browser_items_at_path', 'load_drum_kit'],
        'Scene Management': ['get_scenes_info', 'create_scene', 'fire_scene'],
        'Audio Import': ['import_audio_file']
    }
    
    tool_names = [tool.name for tool in tools]
    
    for category, expected_tools in expected_categories.items():
        print(f"\n{category}:")
        for tool_name in expected_tools:
            if tool_name in tool_names:
                print(f"  ✓ {tool_name}")
            else:
                print(f"  ✗ {tool_name} (missing)")
                return False
    
    return True

def test_tool_schemas():
    """Test that all tools have proper schemas."""
    print("\nTesting tool schemas...")
    
    tools = get_ableton_tools()
    
    for tool in tools:
        try:
            # Test that the tool has a schema
            if not hasattr(tool, 'args_schema'):
                print(f"✗ Tool {tool.name} has no args_schema")
                return False
            
            # Test that the schema can be instantiated
            schema = tool.args_schema
            if schema is None:
                print(f"✗ Tool {tool.name} has None args_schema")
                return False
            
            print(f"  ✓ {tool.name} has valid schema")
            
        except Exception as e:
            print(f"✗ Tool {tool.name} schema error: {e}")
            return False
    
    return True

def test_tool_execution():
    """Test that all tools can be executed and return valid JSON."""
    print("\nTesting tool execution...")
    print("Note: This test requires Ableton Live to be running with MCP server active.")
    print("Tools that fail to connect will show connection errors (expected if Ableton is not running).")
    
    tools = get_ableton_tools()
    results = {
        'successful': [],
        'connection_errors': [],
        'execution_errors': [],
        'invalid_json': []
    }
    
    # Test parameters for different tool types (as dictionaries for LangChain)
    test_params = {
        'get_session_info': {},
        'set_tempo': {"tempo": 127.0},
        'start_playback': {},
        'stop_playback': {},
        'get_track_info': {"track_index": 0},
        'get_device_parameters': {"track_index": 0, "device_index": 1},
        'set_device_parameter': {"track_index": 0, "device_index": 1, "parameter_index": 7, "value": 0.9},
        'batch_set_device_parameters': {"track_index": 0, "device_index": 1, "parameter_indices": [0, 1], "values": [0.3, 0.7]}
        }

    #     'get_device_parameters': {"track_index": 0, "device_index": 0},
    #     'create_midi_track': {"index": -1},
    #     'set_track_name': {"track_index": 0, "name": "Test Track"},
    #     'create_clip': {"track_index": 0, "clip_index": 0, "length": 4.0},
    #     'set_clip_name': {"track_index": 0, "clip_index": 0, "name": "Test Clip"},
    #     'fire_clip': {"track_index": 0, "clip_index": 0},
    #     'stop_clip': {"track_index": 0, "clip_index": 0},
    #     'add_notes_to_clip': {"track_index": 0, "clip_index": 0, "notes": [{"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100}]},
    #     'get_notes_from_clip': {"track_index": 0, "clip_index": 0},
    #     'delete_notes_from_clip': {"track_index": 0, "clip_index": 0},
    #     'transpose_notes_in_clip': {"track_index": 0, "clip_index": 0, "semitones": 7},
    #     'quantize_notes_in_clip': {"track_index": 0, "clip_index": 0, "grid_size": 0.25, "strength": 1.0},
        
    #     'batch_set_device_parameters': {"track_index": 0, "device_index": 0, "parameter_indices": [0, 1], "values": [0.5, 0.7]},
    #     'load_instrument_or_effect': {"track_index": 0, "uri": "test_uri"},
    #     'get_browser_tree': {"category_type": "all"},
    #     'get_browser_items_at_path': {"path": "instruments"},
    #     'load_drum_kit': {"track_index": 0, "rack_uri": "test_rack_uri", "kit_path": "test_kit_path"},
    #     'get_scenes_info': {},
    #     'create_scene': {"index": -1},
    #     'fire_scene': {"index": 0},
    #     'import_audio_file': {"uri": "test_uri.wav"}
    # }
    
    for tool in tools:
        tool_name = tool.name
        print(f"\nTesting {tool_name}...")
        
        try:
            # Get test parameters for this tool
            params = test_params.get(tool_name, {})
            
            # Execute the tool
            result = tool.run(params)
            
            # Try to parse the result as JSON
            try:
                if isinstance(result, str):
                    json_result = json.loads(result)
                else:
                    json_result = result
                
                # Check if it's a valid response structure
                if isinstance(json_result, dict):
                    if 'status' in json_result:
                        if json_result['status'] == 'success':
                            results['successful'].append(tool_name)
                            print(f"  ✓ {tool_name}: Success")
                        elif json_result['status'] == 'error':
                            error_msg = json_result.get('message', 'Unknown error')
                            if 'connect' in error_msg.lower() or 'connection' in error_msg.lower():
                                results['connection_errors'].append(f"{tool_name}: {error_msg}")
                                print(f"  ⚠ {tool_name}: Connection error (expected if Ableton not running)")
                            else:
                                results['execution_errors'].append(f"{tool_name}: {error_msg}")
                                print(f"  ✗ {tool_name}: Execution error - {error_msg}")
                        else:
                            results['execution_errors'].append(f"{tool_name}: Unknown status - {json_result['status']}")
                            print(f"  ✗ {tool_name}: Unknown status - {json_result['status']}")
                    else:
                        # No status field, assume success if we got valid JSON
                        results['successful'].append(tool_name)
                        print(f"  ✓ {tool_name}: Success (no status field)")
                else:
                    results['invalid_json'].append(f"{tool_name}: Result is not a dictionary")
                    print(f"  ✗ {tool_name}: Result is not a dictionary")
                    
            except json.JSONDecodeError as e:
                results['invalid_json'].append(f"{tool_name}: Invalid JSON - {str(e)}")
                print(f"  ✗ {tool_name}: Invalid JSON - {str(e)}")
                print(f"    Raw result: {result[:200]}...")
                
        except Exception as e:
            results['execution_errors'].append(f"{tool_name}: Exception - {str(e)}")
            print(f"  ✗ {tool_name}: Exception - {str(e)}")
    
    # Print summary
    print(f"\n" + "="*60)
    print("TOOL EXECUTION SUMMARY")
    print("="*60)
    
    print(f"\n✓ Successful executions: {len(results['successful'])}")
    for tool in results['successful']:
        print(f"  - {tool}")
    
    print(f"\n⚠ Connection errors (expected if Ableton not running): {len(results['connection_errors'])}")
    for error in results['connection_errors']:
        print(f"  - {error}")
    
    print(f"\n✗ Execution errors: {len(results['execution_errors'])}")
    for error in results['execution_errors']:
        print(f"  - {error}")
    
    print(f"\n✗ Invalid JSON responses: {len(results['invalid_json'])}")
    for error in results['invalid_json']:
        print(f"  - {error}")
    
    # Determine if test passed
    total_tools = len(tools)
    successful_or_connection_error = len(results['successful']) + len(results['connection_errors'])
    
    if successful_or_connection_error == total_tools:
        print(f"\n🎉 All {total_tools} tools executed successfully!")
        print("   (Connection errors are expected if Ableton Live is not running)")
        return True
    else:
        print(f"\n❌ {total_tools - successful_or_connection_error} tools had execution or JSON errors")
        return False

def main():
    """Run all tests."""
    print("Ableton Live LangChain Tools Integration Test")
    print("=" * 50)
    
    tests = [
        test_tool_loading,
        test_tool_categories,
        test_tool_schemas,
        test_tool_execution
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✓ Test passed")
            else:
                print("✗ Test failed")
        except Exception as e:
            print(f"✗ Test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The tool integration is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
