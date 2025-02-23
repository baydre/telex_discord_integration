import os, json, logging
import requests
from fastapi import FastAPI, Request

# Get environment variable (Render automatically provides it)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app =FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/telex-webhook")
async def telex_webhook(request: Request):
    # Receive the message from Telex
    telex_message = await request.json()

    # Log the received message
    logging.info(f"Received message: {telex_message}")


    # Prepare the message for Discord
    discord_message = {
        "content": telex_message.get("content", "🚨 Alert! New Telex message"),
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
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)