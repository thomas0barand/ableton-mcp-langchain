#!/usr/bin/env python3
"""
Test Connection to AbletonMCP
Simple script to test if the connection to Ableton Live works.
"""

from ableton_mcp_client import AbletonMCPClient
import json

def test_connection():
    """Test connection to Ableton Live"""
    print("Testing connection to Ableton Live...")
    print("=" * 50)
    
    client = AbletonMCPClient()
    
    try:
        # Test TCP connection
        print("1. Testing TCP connection...")
        if client.connect_tcp():
            print("   ✓ TCP connection successful")
            
            # Test basic command
            print("2. Testing get_session_info command...")
            session_info = client.get_session_info()
            
            if session_info.get("status") == "success":
                print("   ✓ Command successful")
                print("   Session info:")
                print(json.dumps(session_info["result"], indent=2))
            else:
                print("   ✗ Command failed:", session_info.get("message"))
            
            # Test UDP connection
            print("3. Testing UDP connection...")
            if client.connect_udp():
                print("   ✓ UDP connection successful")
            else:
                print("   ✗ UDP connection failed")
            
        else:
            print("   ✗ TCP connection failed")
            print("\nTroubleshooting:")
            print("- Make sure Ableton Live is running")
            print("- Check that AbletonMCP remote script is installed and active")
            print("- Verify the script is listening on port 9877")
            return False
        
        print("\n" + "=" * 50)
        print("✓ All tests passed! AbletonMCP is working correctly.")
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    finally:
        client.disconnect()

if __name__ == "__main__":
    test_connection()
