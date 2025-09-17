#!/usr/bin/env python3
"""
AbletonMCP Client
A comprehensive client for accessing Ableton Live via the AbletonMCP remote script.
This script provides individual access to all available AbletonMCP tools.
"""

import socket
import json
import time
import sys
from typing import Dict, Any, List, Optional, Union

class AbletonMCPClient:
    """Client for communicating with Ableton Live via AbletonMCP remote script"""
    
    def __init__(self, host: str = "localhost", tcp_port: int = 9877, udp_port: int = 9878):
        """
        Initialize the AbletonMCP client
        
        Args:
            host: Host address (default: localhost)
            tcp_port: TCP port for reliable communication (default: 9877)
            udp_port: UDP port for fast parameter updates (default: 9878)
        """
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.tcp_socket = None
        self.udp_socket = None
        
    def connect_tcp(self) -> bool:
        """Connect to the TCP server"""
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((self.host, self.tcp_port))
            print(f"Connected to AbletonMCP TCP server on {self.host}:{self.tcp_port}")
            return True
        except Exception as e:
            print(f"Failed to connect to TCP server: {e}")
            return False
    
    def connect_udp(self) -> bool:
        """Connect to the UDP server"""
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Connected to AbletonMCP UDP server on {self.host}:{self.udp_port}")
            return True
        except Exception as e:
            print(f"Failed to connect to UDP server: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from servers"""
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
                print("Disconnected from TCP server")
            except:
                pass
            self.tcp_socket = None
            
        if self.udp_socket:
            try:
                self.udp_socket.close()
                print("Disconnected from UDP server")
            except:
                pass
            self.udp_socket = None
    
    def _send_tcp_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command via TCP and return the response"""
        if not self.tcp_socket:
            raise ConnectionError("Not connected to TCP server")
        
        try:
            # Send command
            command_json = json.dumps(command)
            self.tcp_socket.sendall(command_json.encode('utf-8'))
            
            # Receive response
            response_data = b""
            while True:
                chunk = self.tcp_socket.recv(8192)
                if not chunk:
                    break
                response_data += chunk
                try:
                    # Try to parse the complete response
                    response = json.loads(response_data.decode('utf-8'))
                    return response
                except json.JSONDecodeError:
                    # Continue receiving if JSON is incomplete
                    continue
                    
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _send_udp_command(self, command: Dict[str, Any]) -> bool:
        """Send a command via UDP (fire and forget)"""
        if not self.udp_socket:
            raise ConnectionError("Not connected to UDP server")
        
        try:
            command_json = json.dumps(command)
            self.udp_socket.sendto(command_json.encode('utf-8'), (self.host, self.udp_port))
            return True
        except Exception as e:
            print(f"UDP send error: {e}")
            return False
    
    # === SESSION MANAGEMENT ===
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current Ableton Live session"""
        command = {"type": "get_session_info"}
        return self._send_tcp_command(command)
    
    def set_tempo(self, tempo: float) -> Dict[str, Any]:
        """Set the session tempo"""
        command = {
            "type": "set_tempo",
            "params": {"tempo": tempo}
        }
        return self._send_tcp_command(command)
    
    def start_playback(self) -> Dict[str, Any]:
        """Start playback"""
        command = {"type": "start_playback"}
        return self._send_tcp_command(command)
    
    def stop_playback(self) -> Dict[str, Any]:
        """Stop playback"""
        command = {"type": "stop_playback"}
        return self._send_tcp_command(command)
    
    # === TRACK MANAGEMENT ===
    
    def get_track_info(self, track_index: int) -> Dict[str, Any]:
        """Get information about a specific track"""
        command = {
            "type": "get_track_info",
            "params": {"track_index": track_index}
        }
        return self._send_tcp_command(command)
    
    def create_midi_track(self, index: int = -1) -> Dict[str, Any]:
        """Create a new MIDI track"""
        command = {
            "type": "create_midi_track",
            "params": {"index": index}
        }
        return self._send_tcp_command(command)
    
    def create_audio_track(self, index: int = -1) -> Dict[str, Any]:
        """Create a new audio track"""
        command = {
            "type": "create_audio_track",
            "params": {"index": index}
        }
        return self._send_tcp_command(command)
    
    def set_track_name(self, track_index: int, name: str) -> Dict[str, Any]:
        """Set the name of a track"""
        command = {
            "type": "set_track_name",
            "params": {"track_index": track_index, "name": name}
        }
        return self._send_tcp_command(command)
    
    def set_track_level(self, track_index: int, level: float) -> Dict[str, Any]:
        """Set the volume level of a track (0.0 to 1.0)"""
        command = {
            "type": "set_track_level",
            "params": {"track_index": track_index, "level": level}
        }
        return self._send_tcp_command(command)
    
    def set_track_pan(self, track_index: int, pan: float) -> Dict[str, Any]:
        """Set the pan of a track (-1.0 to 1.0)"""
        command = {
            "type": "set_track_pan",
            "params": {"track_index": track_index, "pan": pan}
        }
        return self._send_tcp_command(command)
    
    # === CLIP MANAGEMENT ===
    
    def create_clip(self, track_index: int, clip_index: int, length: float = 4.0) -> Dict[str, Any]:
        """Create a new MIDI clip"""
        command = {
            "type": "create_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "length": length
            }
        }
        return self._send_tcp_command(command)
    
    def set_clip_name(self, track_index: int, clip_index: int, name: str) -> Dict[str, Any]:
        """Set the name of a clip"""
        command = {
            "type": "set_clip_name",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "name": name
            }
        }
        return self._send_tcp_command(command)
    
    def fire_clip(self, track_index: int, clip_index: int) -> Dict[str, Any]:
        """Fire (start) a clip"""
        command = {
            "type": "fire_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index
            }
        }
        return self._send_tcp_command(command)
    
    def stop_clip(self, track_index: int, clip_index: int) -> Dict[str, Any]:
        """Stop a clip"""
        command = {
            "type": "stop_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index
            }
        }
        return self._send_tcp_command(command)
    
    def set_clip_loop_parameters(self, track_index: int, clip_index: int, 
                                loop_start: float, loop_end: float, 
                                loop_enabled: bool = True) -> Dict[str, Any]:
        """Set loop parameters for a clip"""
        command = {
            "type": "set_clip_loop_parameters",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "loop_start": loop_start,
                "loop_end": loop_end,
                "loop_enabled": loop_enabled
            }
        }
        return self._send_tcp_command(command)
    
    def set_clip_follow_action(self, track_index: int, clip_index: int, 
                              action: str, target_clip: Optional[int] = None,
                              chance: float = 1.0, time_val: float = 1.0) -> Dict[str, Any]:
        """Set follow action for a clip"""
        command = {
            "type": "set_clip_follow_action",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "action": action,
                "target_clip": target_clip,
                "chance": chance,
                "time": time_val
            }
        }
        return self._send_tcp_command(command)
    
    # === NOTE MANAGEMENT ===
    
    def add_notes_to_clip(self, track_index: int, clip_index: int, 
                         notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add MIDI notes to a clip"""
        command = {
            "type": "add_notes_to_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "notes": notes
            }
        }
        return self._send_tcp_command(command)
    
    def get_notes_from_clip(self, track_index: int, clip_index: int) -> Dict[str, Any]:
        """Get notes from a clip"""
        command = {
            "type": "get_notes_from_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index
            }
        }
        return self._send_tcp_command(command)
    
    def batch_edit_notes_in_clip(self, track_index: int, clip_index: int,
                                note_ids: List[int], note_data_array: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch edit notes in a clip"""
        command = {
            "type": "batch_edit_notes_in_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "note_ids": note_ids,
                "note_data_array": note_data_array
            }
        }
        return self._send_tcp_command(command)
    
    def delete_notes_from_clip(self, track_index: int, clip_index: int,
                              from_time: Optional[float] = None, to_time: Optional[float] = None,
                              from_pitch: Optional[int] = None, to_pitch: Optional[int] = None) -> Dict[str, Any]:
        """Delete notes from a clip"""
        command = {
            "type": "delete_notes_from_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "from_time": from_time,
                "to_time": to_time,
                "from_pitch": from_pitch,
                "to_pitch": to_pitch
            }
        }
        return self._send_tcp_command(command)
    
    def transpose_notes_in_clip(self, track_index: int, clip_index: int, semitones: int,
                               from_time: Optional[float] = None, to_time: Optional[float] = None,
                               from_pitch: Optional[int] = None, to_pitch: Optional[int] = None) -> Dict[str, Any]:
        """Transpose notes in a clip"""
        command = {
            "type": "transpose_notes_in_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "semitones": semitones,
                "from_time": from_time,
                "to_time": to_time,
                "from_pitch": from_pitch,
                "to_pitch": to_pitch
            }
        }
        return self._send_tcp_command(command)
    
    def quantize_notes_in_clip(self, track_index: int, clip_index: int, grid_size: float = 0.25,
                              strength: float = 1.0, from_time: Optional[float] = None,
                              to_time: Optional[float] = None, from_pitch: Optional[int] = None,
                              to_pitch: Optional[int] = None) -> Dict[str, Any]:
        """Quantize notes in a clip"""
        command = {
            "type": "quantize_notes_in_clip",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "grid_size": grid_size,
                "strength": strength,
                "from_time": from_time,
                "to_time": to_time,
                "from_pitch": from_pitch,
                "to_pitch": to_pitch
            }
        }
        return self._send_tcp_command(command)
    
    def randomize_note_timing(self, track_index: int, clip_index: int, amount: float = 0.1,
                             from_time: Optional[float] = None, to_time: Optional[float] = None,
                             from_pitch: Optional[int] = None, to_pitch: Optional[int] = None) -> Dict[str, Any]:
        """Randomize note timing in a clip"""
        command = {
            "type": "randomize_note_timing",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "amount": amount,
                "from_time": from_time,
                "to_time": to_time,
                "from_pitch": from_pitch,
                "to_pitch": to_pitch
            }
        }
        return self._send_tcp_command(command)
    
    def set_note_probability(self, track_index: int, clip_index: int, probability: float = 1.0,
                            from_time: Optional[float] = None, to_time: Optional[float] = None,
                            from_pitch: Optional[int] = None, to_pitch: Optional[int] = None) -> Dict[str, Any]:
        """Set note probability in a clip"""
        command = {
            "type": "set_note_probability",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "probability": probability,
                "from_time": from_time,
                "to_time": to_time,
                "from_pitch": from_pitch,
                "to_pitch": to_pitch
            }
        }
        return self._send_tcp_command(command)
    
    # === DEVICE MANAGEMENT ===
    
    def get_device_parameters(self, track_index: int, device_index: int) -> Dict[str, Any]:
        """Get parameters for a device"""
        command = {
            "type": "get_device_parameters",
            "params": {
                "track_index": track_index,
                "device_index": device_index
            }
        }
        return self._send_tcp_command(command)
    
    def set_device_parameter(self, track_index: int, device_index: int, 
                           parameter_index: int, value: float) -> Dict[str, Any]:
        """Set a device parameter (value should be 0.0 to 1.0)"""
        command = {
            "type": "set_device_parameter",
            "params": {
                "track_index": track_index,
                "device_index": device_index,
                "parameter_index": parameter_index,
                "value": value
            }
        }
        return self._send_tcp_command(command)
    
    def batch_set_device_parameters(self, track_index: int, device_index: int,
                                  parameter_indices: List[int], values: List[float]) -> Dict[str, Any]:
        """Set multiple device parameters at once"""
        command = {
            "type": "batch_set_device_parameters",
            "params": {
                "track_index": track_index,
                "device_index": device_index,
                "parameter_indices": parameter_indices,
                "values": values
            }
        }
        return self._send_tcp_command(command)
    
    def set_device_parameter_udp(self, track_index: int, device_index: int,
                                parameter_index: int, value: float) -> bool:
        """Set a device parameter via UDP (faster for real-time control)"""
        command = {
            "type": "set_device_parameter",
            "params": {
                "track_index": track_index,
                "device_index": device_index,
                "parameter_index": parameter_index,
                "value": value
            }
        }
        return self._send_udp_command(command)
    
    def batch_set_device_parameters_udp(self, track_index: int, device_index: int,
                                       parameter_indices: List[int], values: List[float]) -> bool:
        """Set multiple device parameters via UDP (faster for real-time control)"""
        command = {
            "type": "batch_set_device_parameters",
            "params": {
                "track_index": track_index,
                "device_index": device_index,
                "parameter_indices": parameter_indices,
                "values": values
            }
        }
        return self._send_udp_command(command)
    
    def load_instrument_or_effect(self, track_index: int, uri: str) -> Dict[str, Any]:
        """Load an instrument or effect by URI"""
        command = {
            "type": "load_instrument_or_effect",
            "params": {
                "track_index": track_index,
                "uri": uri
            }
        }
        return self._send_tcp_command(command)
    
    # === BROWSER MANAGEMENT ===
    
    def get_browser_tree(self, category_type: str = "all") -> Dict[str, Any]:
        """Get the browser tree structure"""
        command = {
            "type": "get_browser_tree",
            "params": {"category_type": category_type}
        }
        return self._send_tcp_command(command)
    
    def get_browser_items_at_path(self, path: str) -> Dict[str, Any]:
        """Get browser items at a specific path"""
        command = {
            "type": "get_browser_items_at_path",
            "params": {"path": path}
        }
        return self._send_tcp_command(command)
    
    def load_drum_kit(self, track_index: int, rack_uri: str, kit_path: str) -> Dict[str, Any]:
        """Load a drum kit"""
        command = {
            "type": "load_drum_kit",
            "params": {
                "track_index": track_index,
                "rack_uri": rack_uri,
                "kit_path": kit_path
            }
        }
        return self._send_tcp_command(command)
    
    # === CLIP ENVELOPES ===
    
    def get_clip_envelope(self, track_index: int, clip_index: int, 
                         device_index: int, parameter_index: int) -> Dict[str, Any]:
        """Get clip envelope data"""
        command = {
            "type": "get_clip_envelope",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "device_index": device_index,
                "parameter_index": parameter_index
            }
        }
        return self._send_tcp_command(command)
    
    def add_clip_envelope_point(self, track_index: int, clip_index: int,
                               device_index: int, parameter_index: int,
                               time_val: float, value: float, curve_type: int = 0) -> Dict[str, Any]:
        """Add a point to a clip envelope"""
        command = {
            "type": "add_clip_envelope_point",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "device_index": device_index,
                "parameter_index": parameter_index,
                "time": time_val,
                "value": value,
                "curve_type": curve_type
            }
        }
        return self._send_tcp_command(command)
    
    def clear_clip_envelope(self, track_index: int, clip_index: int,
                           device_index: int, parameter_index: int) -> Dict[str, Any]:
        """Clear a clip envelope"""
        command = {
            "type": "clear_clip_envelope",
            "params": {
                "track_index": track_index,
                "clip_index": clip_index,
                "device_index": device_index,
                "parameter_index": parameter_index
            }
        }
        return self._send_tcp_command(command)
    
    # === SCENE MANAGEMENT ===
    
    def get_scenes_info(self) -> Dict[str, Any]:
        """Get information about scenes"""
        command = {"type": "get_scenes_info"}
        return self._send_tcp_command(command)
    
    def create_scene(self, index: int = -1) -> Dict[str, Any]:
        """Create a new scene"""
        command = {
            "type": "create_scene",
            "params": {"index": index}
        }
        return self._send_tcp_command(command)
    
    def set_scene_name(self, index: int, name: str) -> Dict[str, Any]:
        """Set the name of a scene"""
        command = {
            "type": "set_scene_name",
            "params": {"index": index, "name": name}
        }
        return self._send_tcp_command(command)
    
    def delete_scene(self, index: int) -> Dict[str, Any]:
        """Delete a scene"""
        command = {
            "type": "delete_scene",
            "params": {"index": index}
        }
        return self._send_tcp_command(command)
    
    def fire_scene(self, index: int) -> Dict[str, Any]:
        """Fire (trigger) a scene"""
        command = {
            "type": "fire_scene",
            "params": {"index": index}
        }
        return self._send_tcp_command(command)
    
    # === AUDIO IMPORT ===
    
    def import_audio_file(self, uri: str, track_index: int = -1, 
                         clip_index: int = 0, create_track_if_needed: bool = True) -> Dict[str, Any]:
        """Import an audio file"""
        command = {
            "type": "import_audio_file",
            "params": {
                "uri": uri,
                "track_index": track_index,
                "clip_index": clip_index,
                "create_track_if_needed": create_track_if_needed
            }
        }
        return self._send_tcp_command(command)


def main():
    """Example usage of the AbletonMCP client"""
    client = AbletonMCPClient()
    
    try:
        # Connect to Ableton Live
        if not client.connect_tcp():
            print("Failed to connect to Ableton Live. Make sure:")
            print("1. Ableton Live is running")
            print("2. The AbletonMCP remote script is installed and active")
            print("3. The script is listening on port 9877")
            return
        
        # Connect to UDP for fast parameter updates
        client.connect_udp()
        
        print("Connected to Ableton Live!")
        print("\n=== Session Info ===")
        session_info = client.get_session_info()
        print(json.dumps(session_info, indent=2))
        
        print("\n=== Track Info (first track) ===")
        track_info = client.get_track_info(0)
        print(json.dumps(track_info, indent=2))
        
        print("\n=== Browser Tree ===")
        browser_tree = client.get_browser_tree("instruments")
        print(json.dumps(browser_tree, indent=2))
        
        # Example: Create a simple MIDI track and clip
        print("\n=== Creating MIDI Track ===")
        new_track = client.create_midi_track()
        print(json.dumps(new_track, indent=2))
        
        if new_track.get("status") == "success":
            track_index = new_track["result"]["index"]
            
            print(f"\n=== Creating Clip on Track {track_index} ===")
            new_clip = client.create_clip(track_index, 0, 4.0)
            print(json.dumps(new_clip, indent=2))
            
            if new_clip.get("status") == "success":
                print(f"\n=== Adding Notes to Clip ===")
                notes = [
                    {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
                    {"pitch": 64, "start_time": 1.0, "duration": 0.5, "velocity": 100},
                    {"pitch": 67, "start_time": 2.0, "duration": 0.5, "velocity": 100},
                ]
                add_notes = client.add_notes_to_clip(track_index, 0, notes)
                print(json.dumps(add_notes, indent=2))
                
                print(f"\n=== Firing Clip ===")
                fire_result = client.fire_clip(track_index, 0)
                print(json.dumps(fire_result, indent=2))
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
