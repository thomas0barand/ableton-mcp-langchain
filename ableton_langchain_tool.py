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


def get_ableton_tools() -> List[BaseTool]:
    """Get all available Ableton Live tools for LangChain."""
    return [
        AbletonSessionInfoTool(),
        AbletonTrackInfoTool(),
        AbletonSetTempoTool(),
        AbletonCreateMidiTrackTool(),
        AbletonCreateClipTool(),
        AbletonAddNotesTool(),
        AbletonFireClipTool(),
    ]
