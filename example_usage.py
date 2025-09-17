#!/usr/bin/env python3
"""
Example Usage of AbletonMCP Client
This script demonstrates how to use individual AbletonMCP tools.
"""

from ableton_mcp_client import AbletonMCPClient
import json
import time

def example_session_management():
    """Example of session management functions"""
    client = AbletonMCPClient()
    
    if not client.connect_tcp():
        print("Failed to connect to Ableton Live")
        return
    
    print("=== Session Management Examples ===")
    
    # Get session info
    session_info = client.get_session_info()
    print("Session Info:", json.dumps(session_info, indent=2))
    
    # Set tempo
    tempo_result = client.set_tempo(128.0)
    print("Set Tempo Result:", json.dumps(tempo_result, indent=2))
    
    # Start playback
    playback_result = client.start_playback()
    print("Start Playback Result:", json.dumps(playback_result, indent=2))
    
    time.sleep(2)  # Let it play for 2 seconds
    
    # Stop playback
    stop_result = client.stop_playback()
    print("Stop Playback Result:", json.dumps(stop_result, indent=2))
    
    client.disconnect()

def example_track_management():
    """Example of track management functions"""
    client = AbletonMCPClient()
    
    if not client.connect_tcp():
        print("Failed to connect to Ableton Live")
        return
    
    print("\n=== Track Management Examples ===")
    
    # Get track info for first track
    track_info = client.get_track_info(0)
    print("Track 0 Info:", json.dumps(track_info, indent=2))
    
    # Create a new MIDI track
    new_track = client.create_midi_track()
    print("New Track:", json.dumps(new_track, indent=2))
    
    if new_track.get("status") == "success":
        track_index = new_track["result"]["index"]
        
        # Set track name
        name_result = client.set_track_name(track_index, "My New Track")
        print("Set Track Name:", json.dumps(name_result, indent=2))
        
        # Set track level
        level_result = client.set_track_level(track_index, 0.8)
        print("Set Track Level:", json.dumps(level_result, indent=2))
        
        # Set track pan
        pan_result = client.set_track_pan(track_index, 0.2)
        print("Set Track Pan:", json.dumps(pan_result, indent=2))
    
    client.disconnect()

def example_clip_management():
    """Example of clip management functions"""
    client = AbletonMCPClient()
    
    if not client.connect_tcp():
        print("Failed to connect to Ableton Live")
        return
    
    print("\n=== Clip Management Examples ===")
    
    # Create a clip on track 0, slot 0
    new_clip = client.create_clip(0, 0, 4.0)
    print("New Clip:", json.dumps(new_clip, indent=2))
    
    if new_clip.get("status") == "success":
        # Set clip name
        name_result = client.set_clip_name(0, 0, "My New Clip")
        print("Set Clip Name:", json.dumps(name_result, indent=2))
        
        # Add some notes
        notes = [
            {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
            {"pitch": 64, "start_time": 1.0, "duration": 0.5, "velocity": 100},
            {"pitch": 67, "start_time": 2.0, "duration": 0.5, "velocity": 100},
            {"pitch": 72, "start_time": 3.0, "duration": 0.5, "velocity": 100},
        ]
        add_notes = client.add_notes_to_clip(0, 0, notes)
        print("Add Notes:", json.dumps(add_notes, indent=2))
        
        # Set loop parameters
        loop_result = client.set_clip_loop_parameters(0, 0, 0.0, 2.0, True)
        print("Set Loop Parameters:", json.dumps(loop_result, indent=2))
        
        # Fire the clip
        fire_result = client.fire_clip(0, 0)
        print("Fire Clip:", json.dumps(fire_result, indent=2))
        
        time.sleep(3)  # Let it play
        
        # Stop the clip
        stop_result = client.stop_clip(0, 0)
        print("Stop Clip:", json.dumps(stop_result, indent=2))
    
    client.disconnect()

def example_device_management():
    """Example of device management functions"""
    client = AbletonMCPClient()
    
    if not client.connect_tcp():
        print("Failed to connect to Ableton Live")
        return
    
    print("\n=== Device Management Examples ===")
    
    # Get device parameters for first device on first track
    device_params = client.get_device_parameters(0, 1)
    print("Device Parameters:", json.dumps(device_params["result"]["parameters"], indent=2))
    
    if device_params.get("status") == "success" and device_params["result"].get("parameters"):
        db_value = -10.0
        normalized_value = (db_value + 15.0) / 30.0
        param_result = client.set_device_parameter(0, 1, 7, normalized_value)
        # print("Set Device Parameter:", json.dumps(param_result, indent=2))
        
        # Batch set multiple parameters
        param_indices = [7, 17, 27, 37]
        param_values = [0.2, 0.6, 0.7, 0.9]
        batch_result = client.batch_set_device_parameters(0, 1, param_indices, param_values)
        # print("Batch Set Parameters:", json.dumps(batch_result, indent=2))
    
    client.disconnect()

def example_browser_management():
    """Example of browser management functions"""
    client = AbletonMCPClient()
    
    if not client.connect_tcp():
        print("Failed to connect to Ableton Live")
        return
    
    print("\n=== Browser Management Examples ===")
    
    # Get browser tree for instruments
    browser_tree = client.get_browser_tree("instruments")
    print("Browser Tree (Instruments):", json.dumps(browser_tree, indent=2))
    
    # Get browser items at a specific path
    browser_items = client.get_browser_items_at_path("instruments")
    print("Browser Items at 'instruments':", json.dumps(browser_items, indent=2))
    
    client.disconnect()

def example_udp_parameter_control():
    """Example of UDP parameter control for real-time updates"""
    client = AbletonMCPClient()
    
    if not client.connect_tcp():
        print("Failed to connect to Ableton Live")
        return
    
    if not client.connect_udp():
        print("Failed to connect to UDP server")
        client.disconnect()
        return
    
    print("\n=== UDP Parameter Control Examples ===")
    
    # Simulate real-time parameter changes
    print("Sending real-time parameter changes via UDP...")
    
    for i in range(10):
        # Vary parameter value between 0.0 and 1.0
        value = 0.5 + 0.3 * (i % 2)  # Alternates between 0.5 and 0.8
        
        # Send via UDP (fire and forget)
        success = client.set_device_parameter_udp(0, 0, 0, value)
        print(f"Parameter change {i+1}: {value:.1f} - {'Success' if success else 'Failed'}")
        
        time.sleep(0.1)  # 100ms intervals
    
    client.disconnect()

def main():
    """Run all examples"""
    print("AbletonMCP Client Examples")
    print("=" * 50)
    
    try:
        # Run examples
        # example_session_management()
        # example_track_management()
        # example_clip_management()
        example_device_management()
        # example_browser_management()
        # example_udp_parameter_control()
        
        print("\n" + "=" * 50)
        print("All examples completed!")
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"Error running examples: {e}")

if __name__ == "__main__":
    main()
