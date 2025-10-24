import pickle

with open("model_checkpoint.pkl", "wb") as f:
    pickle.dump(rnn, f)

print("Checkpoint saved!")
