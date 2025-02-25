import os, json, logging
import requests, markdown
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# Get environment variable (Render automatically provides it)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app =FastAPI()

logging.basicConfig(level=logging.INFO)

# Read the README.md file
with open("DOC.md", "r") as file:
    doc_content = file.read()

# Convert Markdown to HTML
readme_html = markdown.markdown(doc_content)


@app.get("/", response_class=HTMLResponse)
async def root():
    return readme_html

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