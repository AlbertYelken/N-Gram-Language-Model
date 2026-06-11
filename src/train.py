import pickle
from model import NGramModel

MODEL_NAME = "Magnum v1."

new_model = NGramModel(6)

with open("models/"+MODEL_NAME+".pk1", "wb") as f:
    pickle.dump(new_model, f)