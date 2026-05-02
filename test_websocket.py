#!/usr/bin/env python3
"""
Simple WebSocket chat test script
This script demonstrates how to connect to the chat WebSocket endpoint
and send/receive messages.
"""

import asyncio
import websockets
import json
import sys

async def test_websocket_chat():
    """Test the WebSocket chat functionality"""
    # Replace with your actual chat group ID
    chat_group_id = "507f1f77bcf86cd799439011"  # Example ObjectId

    uri = f"ws://localhost:8000/chat/ws/{chat_group_id}"

    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to chat group: {chat_group_id}")

            # Send join message
            join_message = {
                "type": "join"
            }
            await websocket.send(json.dumps(join_message))
            print("Sent join message")

            # Listen for messages
            async for message in websocket:
                data = json.loads(message)
                print(f"Received: {data}")

                # You can add more logic here to handle different message types
                if data.get("type") == "joined":
                    print("Successfully joined the chat group!")

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the FastAPI server is running on localhost:8000")

if __name__ == "__main__":
    print("WebSocket Chat Test")
    print("===================")
    print("This script will connect to the chat WebSocket endpoint.")
    print("Make sure to:")
    print("1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("2. Have a valid chat_group_id")
    print()

    asyncio.run(test_websocket_chat())