import os
import requests
from fastapi import FastAPI, Request
import json
from dotenv import load_dotenv

# load env. variables
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app =FastAPI()

@app.post("/telex-webhook")
async def telex_webhook(request: Request):
    # Receive the message from Telex
    telex_message = await request.json()

    # Prepare the message for Discord
    discord_message = {
        "content": telex_message.get("content", "No content provided")
    }

    # Send the message to Discord
    response = requests.post(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(discord_message),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 204:
        return {"status": "Message sent successfully"}
    else:
        return {"status": "Failed to send message", "error": response.text}