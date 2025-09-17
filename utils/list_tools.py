#!/usr/bin/env python3
"""
List All Available AbletonMCP Tools
This script lists all available tools and their usage.
"""

def list_all_tools():
    """List all available AbletonMCP tools"""
    
    tools = {
        "Session Management": [
            ("get_session_info()", "Get information about the current session"),
            ("set_tempo(tempo)", "Set the session tempo in BPM"),
            ("start_playback()", "Start playback"),
            ("stop_playback()", "Stop playback"),
        ],
        
        "Track Management": [
            ("get_track_info(track_index)", "Get information about a specific track"),
            ("create_midi_track(index=-1)", "Create a new MIDI track"),
            ("create_audio_track(index=-1)", "Create a new audio track"),
            ("set_track_name(track_index, name)", "Set the name of a track"),
            ("set_track_level(track_index, level)", "Set track volume (0.0 to 1.0)"),
            ("set_track_pan(track_index, pan)", "Set track pan (-1.0 to 1.0)"),
        ],
        
        "Clip Management": [
            ("create_clip(track_index, clip_index, length)", "Create a new MIDI clip"),
            ("set_clip_name(track_index, clip_index, name)", "Set the name of a clip"),
            ("fire_clip(track_index, clip_index)", "Fire (start) a clip"),
            ("stop_clip(track_index, clip_index)", "Stop a clip"),
            ("set_clip_loop_parameters(...)", "Set loop parameters for a clip"),
            ("set_clip_follow_action(...)", "Set follow action for a clip"),
        ],
        
        "Note Management": [
            ("add_notes_to_clip(track_index, clip_index, notes)", "Add MIDI notes to a clip"),
            ("get_notes_from_clip(track_index, clip_index)", "Get notes from a clip"),
            ("batch_edit_notes_in_clip(...)", "Batch edit notes in a clip"),
            ("delete_notes_from_clip(...)", "Delete notes from a clip"),
            ("transpose_notes_in_clip(...)", "Transpose notes in a clip"),
            ("quantize_notes_in_clip(...)", "Quantize notes in a clip"),
            ("randomize_note_timing(...)", "Randomize note timing"),
            ("set_note_probability(...)", "Set note probability"),
        ],
        
        "Device Management": [
            ("get_device_parameters(track_index, device_index)", "Get parameters for a device"),
            ("set_device_parameter(track_index, device_index, param_index, value)", "Set a device parameter (0.0 to 1.0)"),
            ("batch_set_device_parameters(...)", "Set multiple device parameters at once"),
            ("set_device_parameter_udp(...)", "Fast parameter updates via UDP"),
            ("load_instrument_or_effect(track_index, uri)", "Load an instrument or effect by URI"),
        ],
        
        "Browser Management": [
            ("get_browser_tree(category_type)", "Get the browser tree structure"),
            ("get_browser_items_at_path(path)", "Get browser items at a specific path"),
            ("load_drum_kit(track_index, rack_uri, kit_path)", "Load a drum kit"),
        ],
        
        "Clip Envelopes": [
            ("get_clip_envelope(track_index, clip_index, device_index, parameter_index)", "Get clip envelope data"),
            ("add_clip_envelope_point(...)", "Add a point to a clip envelope"),
            ("clear_clip_envelope(...)", "Clear a clip envelope"),
        ],
        
        "Scene Management": [
            ("get_scenes_info()", "Get information about scenes"),
            ("create_scene(index=-1)", "Create a new scene"),
            ("set_scene_name(index, name)", "Set the name of a scene"),
            ("delete_scene(index)", "Delete a scene"),
            ("fire_scene(index)", "Fire (trigger) a scene"),
        ],
        
        "Audio Import": [
            ("import_audio_file(uri, track_index, clip_index, create_track_if_needed)", "Import an audio file"),
        ],
    }
    
    print("AbletonMCP Available Tools")
    print("=" * 60)
    print()
    
    for category, tool_list in tools.items():
        print(f"📁 {category}")
        print("-" * 40)
        for tool_name, description in tool_list:
            print(f"  • {tool_name}")
            print(f"    {description}")
        print()
    
    print("=" * 60)
    print("Usage Examples:")
    print()
    print("1. Basic usage:")
    print("   from ableton_mcp_client import AbletonMCPClient")
    print("   client = AbletonMCPClient()")
    print("   client.connect_tcp()")
    print("   result = client.get_session_info()")
    print("   client.disconnect()")
    print()
    print("2. Simple tools:")
    print("   from simple_tools import connect, get_session, set_tempo")
    print("   connect()")
    print("   session = get_session()")
    print("   set_tempo(120)")
    print()
    print("3. Test connection:")
    print("   python test_connection.py")
    print()
    print("4. Run examples:")
    print("   python example_usage.py")
    print("   python simple_tools.py")

if __name__ == "__main__":
    list_all_tools()
