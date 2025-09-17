#!/usr/bin/env python3
"""
Simple AbletonMCP Tools
Quick access to individual AbletonMCP tools for easy use.
"""

from ableton_mcp_client import AbletonMCPClient
import json

# Global client instance
client = None

def connect():
    """Connect to Ableton Live"""
    global client
    client = AbletonMCPClient()
    if client.connect_tcp():
        print("Connected to Ableton Live")
        client.connect_udp()  # Also connect UDP for fast parameter updates
        return True
    else:
        print("Failed to connect to Ableton Live")
        return False

def disconnect():
    """Disconnect from Ableton Live"""
    global client
    if client:
        client.disconnect()
        client = None

# === QUICK ACCESS FUNCTIONS ===

def get_session():
    """Get session information"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.get_session_info()

def set_tempo(bpm):
    """Set session tempo"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.set_tempo(bpm)

def play():
    """Start playback"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.start_playback()

def stop():
    """Stop playback"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.stop_playback()

def get_track(track_index):
    """Get track information"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.get_track_info(track_index)

def create_track(name=None):
    """Create a new MIDI track"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    
    result = client.create_midi_track()
    if result.get("status") == "success" and name:
        track_index = result["result"]["index"]
        client.set_track_name(track_index, name)
    return result

def create_clip(track_index, clip_index=0, length=4.0, name=None):
    """Create a new clip"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    
    result = client.create_clip(track_index, clip_index, length)
    if result.get("status") == "success" and name:
        client.set_clip_name(track_index, clip_index, name)
    return result

def add_notes(track_index, clip_index, notes):
    """Add notes to a clip"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.add_notes_to_clip(track_index, clip_index, notes)

def fire_clip(track_index, clip_index):
    """Fire (start) a clip"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.fire_clip(track_index, clip_index)

def stop_clip(track_index, clip_index):
    """Stop a clip"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.stop_clip(track_index, clip_index)

def get_device_params(track_index, device_index):
    """Get device parameters"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.get_device_parameters(track_index, device_index)

def set_param(track_index, device_index, param_index, value):
    """Set a device parameter (0.0 to 1.0)"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.set_device_parameter(track_index, device_index, param_index, value)

def set_param_fast(track_index, device_index, param_index, value):
    """Set a device parameter via UDP (faster)"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.set_device_parameter_udp(track_index, device_index, param_index, value)

def get_browser(category="all"):
    """Get browser tree"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.get_browser_tree(category)

def load_instrument(track_index, uri):
    """Load an instrument by URI"""
    if not client:
        print("Not connected. Call connect() first.")
        return None
    return client.load_instrument_or_effect(track_index, uri)

# === EXAMPLE USAGE ===

def example():
    """Example usage of the simple tools"""
    print("=== AbletonMCP Simple Tools Example ===")
    
    # Connect
    if not connect():
        return
    
    try:
        # Get session info
        print("\n1. Session Info:")
        session = get_session()
        print(json.dumps(session, indent=2))
        
        # Set tempo
        print("\n2. Setting tempo to 120 BPM:")
        tempo_result = set_tempo(120)
        print(json.dumps(tempo_result, indent=2))
        
        # Create a track
        print("\n3. Creating a new track:")
        track_result = create_track("My Track")
        print(json.dumps(track_result, indent=2))
        
        if track_result.get("status") == "success":
            track_index = track_result["result"]["index"]
            
            # Create a clip
            print(f"\n4. Creating clip on track {track_index}:")
            clip_result = create_clip(track_index, 0, 4.0, "My Clip")
            print(json.dumps(clip_result, indent=2))
            
            # Add some notes
            print(f"\n5. Adding notes to clip:")
            notes = [
                {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
                {"pitch": 64, "start_time": 1.0, "duration": 0.5, "velocity": 100},
                {"pitch": 67, "start_time": 2.0, "duration": 0.5, "velocity": 100},
            ]
            notes_result = add_notes(track_index, 0, notes)
            print(json.dumps(notes_result, indent=2))
            
            # Fire the clip
            print(f"\n6. Firing clip:")
            fire_result = fire_clip(track_index, 0)
            print(json.dumps(fire_result, indent=2))
        
        # Get browser info
        print("\n7. Browser tree (instruments):")
        browser = get_browser("instruments")
        print(json.dumps(browser, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        disconnect()

if __name__ == "__main__":
    example()
