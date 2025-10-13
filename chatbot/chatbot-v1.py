"""
LM Studio Public API + Chat UI Script
-------------------------------------
This script connects to your LM Studio model running locally
and creates a simple web chat interface you can share via ngrok.

👉 Before running:
1️⃣ Make sure LM Studio is open and "Enable Local API Server" is ON.
2️⃣ Check your LM Studio API URL (default: http://localhost:1234/v1).
3️⃣ Install dependencies:
      pip install gradio requests pyngrok
"""

import gradio as gr
import requests
from pyngrok import ngrok

# =====================================
# 🔧 SETTINGS (CHANGE THESE IF NEEDED)
# =====================================

LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"  # 🔧 Change this if LM Studio uses a different port (check in Settings → Developer)
MODEL_NAME = "google/gemma-3n-e4b"  # 🔧 Change to whatever model you loaded in LM Studio
PORT = 7860                                                  # 🔧 Change only if this port is already in use
USE_NGROK = True                                             # 🔧 Set to False if you want LAN-only access (no public link)
USERNAME = "user"                                            # 🔧 Optional: login username
PASSWORD = "1234"                                            # 🔧 Optional: login password (set None to disable auth)

# =====================================
# 🧠 START NGROK (for public sharing)
# =====================================
if USE_NGROK:
    print("🚀 Starting ngrok tunnel...")
    public_url = ngrok.connect(PORT)
    print(f"🔗 Public link: {public_url}")
else:
    print("🌐 Running on local Wi-Fi only (no ngrok)")

# =====================================
# 🤖 FUNCTION TO CALL LM STUDIO API
# =====================================
def chat_with_model(prompt, history=[]):
    """
    Sends chat history + user prompt to LM Studio's local API
    and returns the model's reply.
    """
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": MODEL_NAME, "messages": messages}

    try:
        response = requests.post(LMSTUDIO_API, json=payload, timeout=120)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        history.append((prompt, reply))
        return history, history
    except Exception as e:
        error_msg = f"❌ Error connecting to LM Studio API: {str(e)}"
        history.append((prompt, error_msg))
        return history, history

# =====================================
# 💬 CREATE GRADIO WEB CHAT INTERFACE
# =====================================
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 My Local LM Studio Model Chat")
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(label="Enter your message:")
    clear = gr.Button("🧹 Clear Chat")

    state = gr.State([])
    msg.submit(chat_with_model, [msg, state], [chatbot, state])
    clear.click(lambda: None, None, chatbot)

# =====================================
# 🏁 START THE WEB APP
# =====================================
auth = (USERNAME, PASSWORD) if USERNAME and PASSWORD else None

demo.launch(
    server_name="0.0.0.0",  # allows local + LAN access
    server_port=PORT,
    auth=auth
)
