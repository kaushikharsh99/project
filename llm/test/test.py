import torch
import torch.nn as nn
import torch.optim as optim
import os
import pickle

# ----------------------------
# Vocabulary and encoding
# ----------------------------
vocab = list("abcdefghijklmnopqrstuvwxyz .,!?")
char_to_idx = {c:i for i,c in enumerate(vocab)}
idx_to_char = {i:c for i,c in enumerate(vocab)}

# ----------------------------
# Neural Network: simple char-level RNN
# ----------------------------
class CharRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size=128):
        super().__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(vocab_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, h=None):
        out, h = self.rnn(x, h)
        out = self.fc(out)
        return out, h

# ----------------------------
# Initialize network
# ----------------------------
hidden_size = 128
model_file = "model.pkl"
log_file = "training_data.txt"

if os.path.exists(model_file):
    with open(model_file, "rb") as f:
        rnn = pickle.load(f)
else:
    rnn = CharRNN(len(vocab), hidden_size)

optimizer = optim.Adam(rnn.parameters(), lr=0.005)
criterion = nn.CrossEntropyLoss()

# ----------------------------
# Helpers
# ----------------------------
def text_to_tensor(text):
    idxs = [char_to_idx.get(c,0) for c in text.lower()]
    x = torch.zeros(1, len(idxs), len(vocab))
    for i, idx in enumerate(idxs):
        x[0,i,idx] = 1.0
    return x

def train_on_text(text, epochs=3):
    """Chat/interactive training"""
    # Log training data
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    rnn.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        x = text_to_tensor(text)[:, :-1, :]
        y_idx = [char_to_idx[c] for c in text[1:]]
        y = torch.tensor(y_idx).unsqueeze(0)
        out, _ = rnn(x)
        out = out.view(-1, len(vocab))
        y = y.view(-1)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()

    # Auto-save after training
    with open(model_file, "wb") as f:
        pickle.dump(rnn, f)
    print(f"Trained on: {text} (weights auto-saved)")

def train_on_pairs(input_text, expected_output, epochs=3):
    """Supervised input->output pair training"""
    max_len = max(len(input_text), len(expected_output))
    input_text = input_text.ljust(max_len)
    expected_output = expected_output.ljust(max_len)

    # Log training data
    with open(log_file, "a", encoding="utf-8") as f_log:
        f_log.write(f"PAIR: {input_text} -> {expected_output}\n")

    rnn.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        x = text_to_tensor(input_text)[:, :-1, :]
        y_idx = [char_to_idx.get(c,0) for c in expected_output[1:]]
        y = torch.tensor(y_idx).unsqueeze(0)
        out, _ = rnn(x)
        out = out.view(-1, len(vocab))
        y = y.view(-1)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()

    # Auto-save after training
    with open(model_file, "wb") as f:
        pickle.dump(rnn, f)
    print(f"Trained on pair: {input_text} -> {expected_output} (weights auto-saved)")

def train_from_file_auto(epochs=3):
    """Train on supervised_data.txt if it exists in same folder"""
    filename = "supervised_data.txt"
    if not os.path.exists(filename):
        print(f"No supervised_data.txt found. Skipping file training.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    print(f"Training on {len(lines)} input-output pairs from {filename}...")
    
    for line in lines:
        if "|" not in line:
            print(f"Skipping invalid line: {line}")
            continue
        inp, outp = line.split("|", 1)
        max_len = max(len(inp), len(outp))
        inp = inp.ljust(max_len)
        outp = outp.ljust(max_len)

        # Log training data
        with open(log_file, "a", encoding="utf-8") as f_log:
            f_log.write(f"PAIR: {inp} -> {outp}\n")

        rnn.train()
        for _ in range(epochs):
            optimizer.zero_grad()
            x = text_to_tensor(inp)[:, :-1, :]
            y_idx = [char_to_idx.get(c,0) for c in outp[1:]]
            y = torch.tensor(y_idx).unsqueeze(0)
            out, _ = rnn(x)
            out = out.view(-1, len(vocab))
            y = y.view(-1)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()

    with open(model_file, "wb") as f:
        pickle.dump(rnn, f)
    print(f"Finished training from {filename}, weights saved.")

def generate_dynamic(start="h", min_length=20, max_length=200):
    """Dynamic-length generation, stops at sentence-ending punctuation"""
    rnn.eval()
    idx = char_to_idx.get(start,0)
    x = torch.zeros(1,1,len(vocab))
    x[0,0,idx] = 1
    h = None
    out_text = start

    while True:
        out, h = rnn(x,h)
        probs = torch.softmax(out[0,-1], dim=0)
        idx = torch.multinomial(probs,1).item()
        char = idx_to_char[idx]
        out_text += char
        x = torch.zeros(1,1,len(vocab))
        x[0,0,idx] = 1

        if len(out_text) >= min_length and char in ".!?":
            break
        if len(out_text) >= max_length:
            break

    return out_text

def show_last_training(n=5):
    if os.path.exists(log_file):
        with open(log_file,"r",encoding="utf-8") as f:
            lines = f.read().splitlines()
        print("\n--- Last {} training inputs ---".format(n))
        for line in lines[-n:]:
            print(line)
        print("------------------------------\n")

# ----------------------------
# Interactive session
# ----------------------------
print("Scratch Neural Network Trainer")
show_last_training()

# Auto-train from file if exists
train_from_file_auto()

while True:
    print("\nChoose training mode:")
    print("1: Chat/interactive training")
    print("2: Supervised input->output pair training")
    print("3: Generate text")
    print("4: Exit")
    choice = input("Your choice: ").strip()

    if choice == "1":
        user_input = input("You: ")
        if user_input.lower() in ["exit","quit"]:
            continue
        train_on_text(user_input)
        try:
            min_len = int(input("Minimum characters to generate (e.g., 20): ").strip())
            max_len = int(input("Maximum characters to generate (e.g., 200): ").strip())
        except:
            min_len, max_len = 20, 200
        response = generate_dynamic(start=user_input[0], min_length=min_len, max_length=max_len)
        print("AI:", response)

    elif choice == "2":
        inp = input("Input text: ")
        outp = input("Expected output: ")
        train_on_pairs(inp, outp)
        try:
            min_len = int(input("Minimum characters to generate (e.g., 20): ").strip())
            max_len = int(input("Maximum characters to generate (e.g., 200): ").strip())
        except:
            min_len, max_len = 20, 200
        response = generate_dynamic(start=inp[0], min_length=min_len, max_length=max_len)
        print("AI:", response)

    elif choice == "3":
        start = input("Start character: ").strip()
        try:
            min_len = int(input("Minimum characters to generate (e.g., 20): ").strip())
            max_len = int(input("Maximum characters to generate (e.g., 200): ").strip())
        except:
            min_len, max_len = 20, 200
        response = generate_dynamic(start=start if start else "h", min_length=min_len, max_length=max_len)
        print("AI:", response)

    elif choice == "4":
        print("Session ended. Model saved.")
        break

    else:
        print("Invalid choice. Try again.")
