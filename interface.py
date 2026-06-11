import sys
import pickle

from src import model
sys.modules['model'] = model  

from src.model import NGramModel  

print("Hello, welcome to this N-Gram Language Model chatroom. Type TERMINATE to leave.")

with open("models/Magnum v1..pk1", "rb") as f:
    loaded_model = pickle.load(f)

user_input = ""  
while True:
    user_input = input("You: ")  

    if user_input == "TERMINATE":
        break
    
    user_input = "<P>" + user_input + "<P>" + "<R>"
    print(loaded_model.respond(user_input))