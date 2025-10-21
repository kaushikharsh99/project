# chatbot-v4.py
import json
import time
import sys
import requests
import gradio as gr
from pyngrok import ngrok

# ----------------------------
# SETTINGS
# ----------------------------
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "llama-3-8b-lexi-uncensored"
PORT = 7860

# ----------------------------
# START NGROK (optional)
# ----------------------------
print("🚀 Starting ngrok tunnel...")
public_url = ngrok.connect(PORT)
print(f"🔗 Public link: {public_url}")

# ----------------------------
# STREAMING CHAT FUNCTION
# ----------------------------
def chat_with_model(prompt, history=None):
    """
    history: list of (user_text, bot_text) tuples
    This generator yields (chat_history, history_state, textbox_value)
    """
    if history is None:
        history = []
    print("=============================================================================")
    print(f"[USER PROMPT] {prompt}")
    print("=============================================================================")
    print(".")
    print(".")
    sys.stdout.flush()

    # Build messages in OpenAI-style for LM Studio
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for user_text, bot_text in history:
        messages.append({"role": "user", "content": user_text})
        messages.append({"role": "assistant", "content": bot_text})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": MODEL_NAME, "messages": messages, "stream": True}
    reply = ""

    try:
        with requests.post(LMSTUDIO_API, json=payload, stream=True, timeout=(10, 600)) as r:
            r.raise_for_status()
            print("[STREAM] Connected to LM Studio, reading stream...")
            sys.stdout.flush()

            # iter_lines with decode_unicode=True usually yields lines as they arrive
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue

                # LM Studio streaming lines normally start with 'data: '
                # but some setups may send bare JSON lines; handle both.
                raw = line.strip()
                if raw.startswith("data: "):
                    data = raw[len("data: "):].strip()
                else:
                    data = raw

                if not data:
                    continue

                if data == "[DONE]":
                    print("[STREAM] Received [DONE]")
                    break

                # Try to parse JSON chunk
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    # ignore invalid json chunk lines
                    print("[STREAM] JSON decode error for chunk:", data[:200])
                    sys.stdout.flush()
                    continue

                # Two common streaming formats:
                # 1) chunk["choices"][0]["delta"]["content"]  (streaming token deltas)
                # 2) chunk["choices"][0]["message"]["content"] (some servers)
                delta = ""
                try:
                    delta = chunk["choices"][0].get("delta", {}).get("content", "")
                except Exception:
                    delta = ""

                if not delta:
                    # fallback: maybe full message chunk present
                    try:
                        delta = chunk["choices"][0].get("message", {}).get("content", "")
                    except Exception:
                        delta = ""

                if not delta:
                    # nothing to show this iteration (e.g., only role info) — continue
                    continue

                # append delta and yield immediately
                reply += delta

                # 🔹 print live response in terminal
                print(delta, end="", flush=True)

                # Build chat display as list of tuples for gr.Chatbot
                chat_display = [(u, b) for (u, b) in history]
                chat_display.append((prompt, reply))

                # Yield partial update to Gradio
                yield chat_display, history, ""
                time.sleep(0.01)

    except requests.exceptions.Timeout:
        reply = "⚠️ The model took too long to respond (timeout)."
        print("[ERROR] Timeout")
    except requests.exceptions.ConnectionError:
        reply = "❌ Could not connect to LM Studio. Is the API server running?"
        print("[ERROR] ConnectionError")
    except Exception as e:
        reply = f"❌ Error: {e}"
        print("[ERROR] Exception:", e)
    finally:
        history.append((prompt, reply))
        # 🔹 print full AI reply summary once done
        print("\n=============================================================================")
        print(f"[AI REPLY COMPLETED] {reply}")
        print("=============================================================================")


    # Final yield with full history
    chat_display = [(u, b) for (u, b) in history]
    yield chat_display, history, ""

# ----------------------------
# GRADIO UI
# ----------------------------
with gr.Blocks(title="Local LM Studio Chat (Streaming)") as demo:
    gr.Markdown("## 🤖 Local LM Studio Chatbot\nType below and press **Enter** or click **Send**")
    gr.Markdown(f"**ngrok public URL:** {public_url}")

    chatbot = gr.Chatbot(elem_id="chatbot", height=500)
    user_input = gr.Textbox(placeholder="Type your message...", lines=1, show_label=False)
    send_btn = gr.Button("Send 🚀")
    state = gr.State([])  # history as list of tuples

    # IMPORTANT: queue=True is required for generator streaming to work
    user_input.submit(chat_with_model, [user_input, state], [chatbot, state, user_input], queue=True)
    send_btn.click(chat_with_model, [user_input, state], [chatbot, state, user_input], queue=True)

# ----------------------------
# LAUNCH
# ----------------------------
demo.launch(server_name="0.0.0.0", server_port=PORT)
