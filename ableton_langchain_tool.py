#!/usr/bin/env python3
"""
LangChain Tool Wrapper for AbletonMCP Client
This module provides LangChain tools that wrap the AbletonMCP client functionality.
"""

from typing import Type, Optional, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ableton_mcp_client import AbletonMCPClient
import json


class SessionInfoInput(BaseModel):
    """Input for getting session information."""
    pass


class TrackInfoInput(BaseModel):
    """Input for getting track information."""
    track_index: int = Field(description="The index of the track to get information about")


class SetTempoInput(BaseModel):
    """Input for setting session tempo."""
    tempo: float = Field(description="The tempo in BPM to set")


class CreateMidiTrackInput(BaseModel):
    """Input for creating a MIDI track."""
    index: int = Field(default=-1, description="The index to insert the track at (-1 = end of list)")


class CreateClipInput(BaseModel):
    """Input for creating a MIDI clip."""
    track_index: int = Field(description="The index of the track to create the clip in")
    clip_index: int = Field(description="The index of the clip slot to create the clip in")
    length: float = Field(default=4.0, description="The length of the clip in beats")


class AddNotesInput(BaseModel):
    """Input for adding notes to a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")
    notes: List[Dict[str, Any]] = Field(description="List of note dictionaries with pitch, start_time, duration, velocity, and mute")


class FireClipInput(BaseModel):
    """Input for firing a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")


class StopClipInput(BaseModel):
    """Input for stopping a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")


class SetTrackNameInput(BaseModel):
    """Input for setting track name."""
    track_index: int = Field(description="The index of the track to rename")
    name: str = Field(description="The new name for the track")


class SetClipNameInput(BaseModel):
    """Input for setting clip name."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")
    name: str = Field(description="The new name for the clip")


class GetDeviceParametersInput(BaseModel):
    """Input for getting device parameters."""
    track_index: int = Field(description="The index of the track containing the device")
    device_index: int = Field(description="The index of the device on the track")


class SetDeviceParameterInput(BaseModel):
    """Input for setting a device parameter."""
    track_index: int = Field(description="The index of the track containing the device")
    device_index: int = Field(description="The index of the device on the track")
    parameter_index: int = Field(description="The index of the parameter to set")
    value: float = Field(description="Normalized value between 0.0 and 1.0")


class BatchSetDeviceParametersInput(BaseModel):
    """Input for setting multiple device parameters."""
    track_index: int = Field(description="The index of the track containing the device")
    device_index: int = Field(description="The index of the device on the track")
    parameter_indices: List[int] = Field(description="List of parameter indices to set")
    values: List[float] = Field(description="List of normalized values (0.0 to 1.0)")


class LoadInstrumentOrEffectInput(BaseModel):
    """Input for loading an instrument or effect."""
    track_index: int = Field(description="The index of the track to load the instrument on")
    uri: str = Field(description="The URI of the instrument or effect to load")


class GetBrowserTreeInput(BaseModel):
    """Input for getting browser tree."""
    category_type: str = Field(default="all", description="Type of categories to get ('all', 'instruments', 'sounds', 'drums', 'audio_effects', 'midi_effects')")


class GetBrowserItemsAtPathInput(BaseModel):
    """Input for getting browser items at path."""
    path: str = Field(description="Path in the format 'category/folder/subfolder'")


class LoadDrumKitInput(BaseModel):
    """Input for loading a drum kit."""
    track_index: int = Field(description="The index of the track to load on")
    rack_uri: str = Field(description="The URI of the drum rack to load")
    kit_path: str = Field(description="Path to the drum kit inside the browser")


class GetNotesFromClipInput(BaseModel):
    """Input for getting notes from a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")


class DeleteNotesFromClipInput(BaseModel):
    """Input for deleting notes from a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")
    from_time: Optional[float] = Field(default=None, description="Start time for deletion range")
    to_time: Optional[float] = Field(default=None, description="End time for deletion range")
    from_pitch: Optional[int] = Field(default=None, description="Start pitch for deletion range")
    to_pitch: Optional[int] = Field(default=None, description="End pitch for deletion range")


class TransposeNotesInput(BaseModel):
    """Input for transposing notes in a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")
    semitones: int = Field(description="Number of semitones to transpose")
    from_time: Optional[float] = Field(default=None, description="Start time for transpose range")
    to_time: Optional[float] = Field(default=None, description="End time for transpose range")
    from_pitch: Optional[int] = Field(default=None, description="Start pitch for transpose range")
    to_pitch: Optional[int] = Field(default=None, description="End pitch for transpose range")


class QuantizeNotesInput(BaseModel):
    """Input for quantizing notes in a clip."""
    track_index: int = Field(description="The index of the track containing the clip")
    clip_index: int = Field(description="The index of the clip slot containing the clip")
    grid_size: float = Field(default=0.25, description="Grid size for quantization")
    strength: float = Field(default=1.0, description="Quantization strength (0.0 to 1.0)")
    from_time: Optional[float] = Field(default=None, description="Start time for quantization range")
    to_time: Optional[float] = Field(default=None, description="End time for quantization range")
    from_pitch: Optional[int] = Field(default=None, description="Start pitch for quantization range")
    to_pitch: Optional[int] = Field(default=None, description="End pitch for quantization range")


class GetScenesInfoInput(BaseModel):
    """Input for getting scenes information."""
    pass


class CreateSceneInput(BaseModel):
    """Input for creating a scene."""
    index: int = Field(default=-1, description="The index to insert the scene at (-1 = end of list)")


class FireSceneInput(BaseModel):
    """Input for firing a scene."""
    index: int = Field(description="The index of the scene to fire")


class ImportAudioFileInput(BaseModel):
    """Input for importing an audio file."""
    uri: str = Field(description="The URI of the audio file to import")
    track_index: int = Field(default=-1, description="The index of the track to import to (-1 = create new track)")
    clip_index: int = Field(default=0, description="The index of the clip slot to import to")
    create_track_if_needed: bool = Field(default=True, description="Whether to create a new track if needed")


class AbletonSessionInfoTool(BaseTool):
    """Tool for getting Ableton Live session information."""
    name: str = "get_session_info"
    description: str = "Get information about the current Ableton Live session including tempo, tracks, and other session details."
    args_schema: Type[BaseModel] = SessionInfoInput

    def _run(self) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_session_info()
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonTrackInfoTool(BaseTool):
    """Tool for getting track information."""
    name: str = "get_track_info"
    description: str = "Get detailed information about a specific track in Ableton Live."
    args_schema: Type[BaseModel] = TrackInfoInput

    def _run(self, track_index: int) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_track_info(track_index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonSetTempoTool(BaseTool):
    """Tool for setting session tempo."""
    name: str = "set_tempo"
    description: str = "Set the tempo of the Ableton Live session."
    args_schema: Type[BaseModel] = SetTempoInput

    def _run(self, tempo: float) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.set_tempo(tempo)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonCreateMidiTrackTool(BaseTool):
    """Tool for creating a MIDI track."""
    name: str = "create_midi_track"
    description: str = "Create a new MIDI track in the Ableton Live session."
    args_schema: Type[BaseModel] = CreateMidiTrackInput

    def _run(self, index: int = -1) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.create_midi_track(index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonCreateClipTool(BaseTool):
    """Tool for creating a MIDI clip."""
    name: str = "create_clip"
    description: str = "Create a new MIDI clip in the specified track and clip slot."
    args_schema: Type[BaseModel] = CreateClipInput

    def _run(self, track_index: int, clip_index: int, length: float = 4.0) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.create_clip(track_index, clip_index, length)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonAddNotesTool(BaseTool):
    """Tool for adding notes to a clip."""
    name: str = "add_notes_to_clip"
    description: str = "Add MIDI notes to a clip. Notes should be provided as a list of dictionaries with pitch, start_time, duration, velocity, and mute fields."
    args_schema: Type[BaseModel] = AddNotesInput

    def _run(self, track_index: int, clip_index: int, notes: List[Dict[str, Any]]) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.add_notes_to_clip(track_index, clip_index, notes)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonFireClipTool(BaseTool):
    """Tool for firing a clip."""
    name: str = "fire_clip"
    description: str = "Start playing a clip in Ableton Live."
    args_schema: Type[BaseModel] = FireClipInput

    def _run(self, track_index: int, clip_index: int) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.fire_clip(track_index, clip_index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonStopClipTool(BaseTool):
    """Tool for stopping a clip."""
    name: str = "stop_clip"
    description: str = "Stop playing a clip in Ableton Live."
    args_schema: Type[BaseModel] = StopClipInput

    def _run(self, track_index: int, clip_index: int) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.stop_clip(track_index, clip_index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonStartPlaybackTool(BaseTool):
    """Tool for starting playback."""
    name: str = "start_playback"
    description: str = "Start playing the Ableton Live session."
    args_schema: Type[BaseModel] = SessionInfoInput  # No parameters needed

    def _run(self) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.start_playback()
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonStopPlaybackTool(BaseTool):
    """Tool for stopping playback."""
    name: str = "stop_playback"
    description: str = "Stop playing the Ableton Live session."
    args_schema: Type[BaseModel] = SessionInfoInput  # No parameters needed

    def _run(self) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.stop_playback()
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonSetTrackNameTool(BaseTool):
    """Tool for setting track name."""
    name: str = "set_track_name"
    description: str = "Set the name of a track in Ableton Live."
    args_schema: Type[BaseModel] = SetTrackNameInput

    def _run(self, track_index: int, name: str) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.set_track_name(track_index, name)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonSetClipNameTool(BaseTool):
    """Tool for setting clip name."""
    name: str = "set_clip_name"
    description: str = "Set the name of a clip in Ableton Live."
    args_schema: Type[BaseModel] = SetClipNameInput

    def _run(self, track_index: int, clip_index: int, name: str) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.set_clip_name(track_index, clip_index, name)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonGetDeviceParametersTool(BaseTool):
    """Tool for getting device parameters."""
    name: str = "get_device_parameters"
    description: str = "Get detailed information about all parameters for a specific device on a track."
    args_schema: Type[BaseModel] = GetDeviceParametersInput

    def _run(self, track_index: int, device_index: int) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_device_parameters(track_index, device_index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonSetDeviceParameterTool(BaseTool):
    """Tool for setting a device parameter."""
    name: str = "set_device_parameter"
    description: str = "Set a single device parameter value using normalized values (0.0 to 1.0)."
    args_schema: Type[BaseModel] = SetDeviceParameterInput

    def _run(self, track_index: int, device_index: int, parameter_index: int, value: float) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.set_device_parameter(track_index, device_index, parameter_index, value)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonBatchSetDeviceParametersTool(BaseTool):
    """Tool for setting multiple device parameters."""
    name: str = "batch_set_device_parameters"
    description: str = "Set multiple device parameters at once using normalized values (0.0 to 1.0)."
    args_schema: Type[BaseModel] = BatchSetDeviceParametersInput

    def _run(self, track_index: int, device_index: int, parameter_indices: List[int], values: List[float]) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.batch_set_device_parameters(track_index, device_index, parameter_indices, values)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonLoadInstrumentOrEffectTool(BaseTool):
    """Tool for loading an instrument or effect."""
    name: str = "load_instrument_or_effect"
    description: str = "Load an instrument or effect onto a track using its URI."
    args_schema: Type[BaseModel] = LoadInstrumentOrEffectInput

    def _run(self, track_index: int, uri: str) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.load_instrument_or_effect(track_index, uri)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonGetBrowserTreeTool(BaseTool):
    """Tool for getting browser tree."""
    name: str = "get_browser_tree"
    description: str = "Get a hierarchical tree of browser categories from Ableton."
    args_schema: Type[BaseModel] = GetBrowserTreeInput

    def _run(self, category_type: str = "all") -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_browser_tree(category_type)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonGetBrowserItemsAtPathTool(BaseTool):
    """Tool for getting browser items at path."""
    name: str = "get_browser_items_at_path"
    description: str = "Get browser items at a specific path in Ableton's browser."
    args_schema: Type[BaseModel] = GetBrowserItemsAtPathInput

    def _run(self, path: str) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_browser_items_at_path(path)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonLoadDrumKitTool(BaseTool):
    """Tool for loading a drum kit."""
    name: str = "load_drum_kit"
    description: str = "Load a drum rack and then load a specific drum kit into it."
    args_schema: Type[BaseModel] = LoadDrumKitInput

    def _run(self, track_index: int, rack_uri: str, kit_path: str) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.load_drum_kit(track_index, rack_uri, kit_path)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonGetNotesFromClipTool(BaseTool):
    """Tool for getting notes from a clip."""
    name: str = "get_notes_from_clip"
    description: str = "Get all notes from a clip in Ableton Live."
    args_schema: Type[BaseModel] = GetNotesFromClipInput

    def _run(self, track_index: int, clip_index: int) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_notes_from_clip(track_index, clip_index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonDeleteNotesFromClipTool(BaseTool):
    """Tool for deleting notes from a clip."""
    name: str = "delete_notes_from_clip"
    description: str = "Delete notes from a clip in Ableton Live."
    args_schema: Type[BaseModel] = DeleteNotesFromClipInput

    def _run(self, track_index: int, clip_index: int, from_time: Optional[float] = None, 
             to_time: Optional[float] = None, from_pitch: Optional[int] = None, 
             to_pitch: Optional[int] = None) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.delete_notes_from_clip(track_index, clip_index, from_time, to_time, from_pitch, to_pitch)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonTransposeNotesTool(BaseTool):
    """Tool for transposing notes in a clip."""
    name: str = "transpose_notes_in_clip"
    description: str = "Transpose notes in a clip by a specified number of semitones."
    args_schema: Type[BaseModel] = TransposeNotesInput

    def _run(self, track_index: int, clip_index: int, semitones: int, 
             from_time: Optional[float] = None, to_time: Optional[float] = None,
             from_pitch: Optional[int] = None, to_pitch: Optional[int] = None) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.transpose_notes_in_clip(track_index, clip_index, semitones, from_time, to_time, from_pitch, to_pitch)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonQuantizeNotesTool(BaseTool):
    """Tool for quantizing notes in a clip."""
    name: str = "quantize_notes_in_clip"
    description: str = "Quantize notes in a clip to a specified grid size."
    args_schema: Type[BaseModel] = QuantizeNotesInput

    def _run(self, track_index: int, clip_index: int, grid_size: float = 0.25, 
             strength: float = 1.0, from_time: Optional[float] = None, 
             to_time: Optional[float] = None, from_pitch: Optional[int] = None, 
             to_pitch: Optional[int] = None) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.quantize_notes_in_clip(track_index, clip_index, grid_size, strength, from_time, to_time, from_pitch, to_pitch)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonGetScenesInfoTool(BaseTool):
    """Tool for getting scenes information."""
    name: str = "get_scenes_info"
    description: str = "Get information about scenes in Ableton Live."
    args_schema: Type[BaseModel] = GetScenesInfoInput

    def _run(self) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.get_scenes_info()
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonCreateSceneTool(BaseTool):
    """Tool for creating a scene."""
    name: str = "create_scene"
    description: str = "Create a new scene in Ableton Live."
    args_schema: Type[BaseModel] = CreateSceneInput

    def _run(self, index: int = -1) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.create_scene(index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonFireSceneTool(BaseTool):
    """Tool for firing a scene."""
    name: str = "fire_scene"
    description: str = "Fire (trigger) a scene in Ableton Live."
    args_schema: Type[BaseModel] = FireSceneInput

    def _run(self, index: int) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.fire_scene(index)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


class AbletonImportAudioFileTool(BaseTool):
    """Tool for importing an audio file."""
    name: str = "import_audio_file"
    description: str = "Import an audio file into Ableton Live."
    args_schema: Type[BaseModel] = ImportAudioFileInput

    def _run(self, uri: str, track_index: int = -1, clip_index: int = 0, 
             create_track_if_needed: bool = True) -> str:
        """Execute the tool."""
        client = AbletonMCPClient()
        try:
            if not client.connect_tcp():
                return "Error: Failed to connect to Ableton Live. Make sure Ableton Live is running and the MCP server is active."
            
            result = client.import_audio_file(uri, track_index, clip_index, create_track_if_needed)
            client.disconnect()
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"


def get_ableton_tools() -> List[BaseTool]:
    """Get all available Ableton Live tools for LangChain."""
    return [
        # Session Management
        AbletonSessionInfoTool(),
        AbletonSetTempoTool(),
        AbletonStartPlaybackTool(),
        AbletonStopPlaybackTool(),
        
        # Track Management
        AbletonTrackInfoTool(),
        AbletonCreateMidiTrackTool(),
        AbletonSetTrackNameTool(),
        
        # Clip Management
        AbletonCreateClipTool(),
        AbletonSetClipNameTool(),
        AbletonFireClipTool(),
        AbletonStopClipTool(),
        
        # Note Management
        AbletonAddNotesTool(),
        AbletonGetNotesFromClipTool(),
        AbletonDeleteNotesFromClipTool(),
        AbletonTransposeNotesTool(),
        AbletonQuantizeNotesTool(),
        
        # Device Management
        AbletonGetDeviceParametersTool(),
        AbletonSetDeviceParameterTool(),
        AbletonBatchSetDeviceParametersTool(),
        AbletonLoadInstrumentOrEffectTool(),
        
        # Browser Management
        AbletonGetBrowserTreeTool(),
        AbletonGetBrowserItemsAtPathTool(),
        AbletonLoadDrumKitTool(),
        
        # Scene Management
        AbletonGetScenesInfoTool(),
        AbletonCreateSceneTool(),
        AbletonFireSceneTool(),
        
        # Audio Import
        AbletonImportAudioFileTool(),
    ]
