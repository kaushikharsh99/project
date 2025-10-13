import json
import time
import requests
import gradio as gr
from pyngrok import ngrok
import os

# ----------------------------
# PATH SETUP
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
HEADER_PATH = os.path.join(STATIC_DIR, "header.html")
CSS_PATH = os.path.join(STATIC_DIR, "style.css")

# ----------------------------
# SETTINGS
# ----------------------------
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "llama-3-8b-lexi-uncensored"
PORT = 7860

# ----------------------------
# START NGROK
# ----------------------------
try:
    public_url = ngrok.connect(PORT).public_url
    print(f"🔗 Public link: {public_url}")
except Exception as e:
    print("⚠️ ngrok failed or already running:", e)
    tunnels = ngrok.get_tunnels()
    if tunnels:
        public_url = tunnels[0].public_url
    else:
        raise e

# ----------------------------
# CHAT FUNCTION (STREAM)
# ----------------------------
def chat_with_model(prompt, history=None):
    if history is None:
        history = []

    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for u, b in history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": MODEL_NAME, "messages": messages, "stream": True}
    reply = ""

    try:
        with requests.post(LMSTUDIO_API, json=payload, stream=True, timeout=(10, 600)) as r:
            r.raise_for_status()
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                data = line.strip()
                if data.startswith("data: "):
                    data = data[len("data: "):]
                if not data or data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0].get("delta", {}).get("content", "")
                except Exception:
                    continue
                if not delta:
                    continue
                reply += delta
                chat_display = history + [(prompt, reply)]
                yield chat_display, history, ""
                time.sleep(0.01)
    except Exception as e:
        reply = f"❌ Error: {e}"

    history.append((prompt, reply))
    yield history, history, ""

# ----------------------------
# GRADIO UI
# ----------------------------
with open(HEADER_PATH, "r", encoding="utf-8") as f:
    header_html = f.read()

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css_data = f.read()

with gr.Blocks(css=css_data, title="ChatGPT-style AI Chatbot") as demo:
    gr.HTML(
        header_html.replace("{{MODEL_NAME}}", MODEL_NAME)
                   .replace("{{PUBLIC_URL}}", public_url)
    )

    chatbot = gr.Chatbot(elem_id="chatbot", height=550, bubble_full_width=False)
    with gr.Row(elem_classes="input-row"):
        user_input = gr.Textbox(placeholder="Type a message...", lines=1, show_label=False)
        send_btn = gr.Button("Send 🚀", variant="primary")
        clear_btn = gr.Button("Clear 🧹", variant="secondary")

    state = gr.State([])

    user_input.submit(chat_with_model, [user_input, state], [chatbot, state, user_input], queue=True)
    send_btn.click(chat_with_model, [user_input, state], [chatbot, state, user_input], queue=True)
    clear_btn.click(lambda: ([], []), None, [chatbot, state])

demo.launch(server_name="0.0.0.0", server_port=PORT)
