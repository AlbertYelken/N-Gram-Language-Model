Written by Albert Yelken, a student researcher and incoming freshman in Georgia Tech's Class of 2030.

LinkedIn: https://www.linkedin.com/in/albertyelken/

Magnum v1.0 is a simple console-based chatbot built using an N-Gram language model. The model is trained on text data stored in `data/raw.txt` and serialized using Python's `pickle` module. To install the required dependency, run `pip install pandas`. Train the model by running `python src/train.py`, which generates the model file in the `models/` directory. Start the chatbot with `python interface.py`, then type messages into the console. Enter `TERMINATE` at any time to exit the chat.
