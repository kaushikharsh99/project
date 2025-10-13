import gradio as gr
import requests
from pyngrok import ngrok

# ----------------------------
# SETTINGS
# ----------------------------
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"   # Change if your LM Studio uses another port
MODEL_NAME = "llama-3.2-3b-instruct-uncensored"                           # Change to your model name
PORT = 7860

# ----------------------------
# CONNECT NGROK (for public link)
# ----------------------------
print("🚀 Starting ngrok tunnel...")
public_url = ngrok.connect(PORT)
print(f"🔗 Public link: {public_url}")

# ----------------------------
# CHAT FUNCTION
# ----------------------------
def chat_with_model(prompt, history=[]):
    # Log user
    print(f"[USER] {prompt}")

    # Prepare conversation
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for msg in history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["bot"]})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": MODEL_NAME, "messages": messages}

    try:
        response = requests.post(LMSTUDIO_API, json=payload, timeout=120)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # Add to history
    history.append({"user": prompt, "bot": reply})

    # ---------- WORD-BY-WORD SIMULATION ----------
    words = reply.split()
    current_reply = ""
    for w in words:
        current_reply += w + " "
        # Build messages for Gradio UI
        chat_messages_display = []
        for h in history[:-1]:
            chat_messages_display.append({"role": "user", "content": h["user"]})
            chat_messages_display.append({"role": "assistant", "content": h["bot"]})
        chat_messages_display.append({"role": "user", "content": prompt})
        chat_messages_display.append({"role": "assistant", "content": current_reply})
        yield chat_messages_display, history, ""  # third "" clears the textbox
        import time
        time.sleep(0.01)  # typing speed (adjust to taste)

    # Final state
    chat_messages_display = []
    for h in history:
        chat_messages_display.append({"role": "user", "content": h["user"]})
        chat_messages_display.append({"role": "assistant", "content": h["bot"]})

    yield chat_messages_display, history, ""


# ----------------------------
# GRADIO UI
# ----------------------------
with gr.Blocks(title="Local AI Chat") as demo:
    gr.Markdown("## 🤖 Local LM Studio Chatbot\nType below and press **Enter** or click **Send**")

    chatbot = gr.Chatbot(height=450, type="messages")
    user_input = gr.Textbox(
        placeholder="Type your message and press Enter or click Send...",
        label="Your Message",
        show_label=False,
        lines=1
    )
    send_btn = gr.Button("Send 🚀")

    state = gr.State([])

    # When pressing Enter or Send button
    user_input.submit(chat_with_model, [user_input, state], [chatbot, state, user_input])
    send_btn.click(chat_with_model, [user_input, state], [chatbot, state, user_input])

# ----------------------------
# LAUNCH
# ----------------------------
demo.launch(server_name="0.0.0.0", server_port=PORT)
