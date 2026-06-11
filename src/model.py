import pandas as pd
import re
import string

class NGramModel:
    PUNCTUATION_PATTERN = re.escape(string.punctuation.replace("'", ""))
    
    def __init__(self, N, data_path="data/raw.txt", max_tokens=50):
        self.N = N
        self.data = self.format_data(data_path)
        self.max_tokens = max_tokens

    def format_data(self, data_path):
        with open(data_path, encoding="utf-8") as f:
            lines = [x.rstrip() for x in f]
            return pd.Series(map(self.create_ngrams, lines)).explode().reset_index(drop=True)
    
    def create_ngrams(self, line):
        pattern = rf"(<P>|<R>|[{self.PUNCTUATION_PATTERN}])| "
        split = re.split(pattern, line)
        tokens = [item for item in split if item and item.strip()]

        if len(tokens) < self.N:
            tokens += ["BLANK"] * (self.N - len(tokens))

        return [tuple(tokens[i : i + self.N]) for i in range(len(tokens) - self.N + 1)]
    
    def predict_token(self, input_text):
        pattern = rf"(<P>|<R>|[{self.PUNCTUATION_PATTERN}])| "
        split = re.split(pattern, input_text)
        input_tokens = [item for item in split if item and item.strip()]
        
        for context_size in range(self.N - 1, 0, -1):
            context = tuple(input_tokens[-context_size:])
            if len(context) < context_size:
                context = tuple(["BLANK"] * (context_size - len(context))) + context
                
            matches = self.data[self.data.apply(
                lambda x: isinstance(x, tuple) and len(x) >= self.N and x[:context_size] == context
            )]
            
            if not matches.empty:
                next_words = matches.apply(lambda x: x[context_size])
                
                next_words = next_words[next_words != "<P>"]
                
                if not next_words.empty:
                    return next_words.value_counts().idxmax()
                
        if not self.data.empty:
            all_tokens = self.data.explode()
            
            all_tokens = all_tokens[all_tokens != "<P>"]
            
            if not all_tokens.empty:
                return all_tokens.value_counts().idxmax()
                
        return "BLANK"
    
    def respond(self, input_text):
        i = 0
        response = ""
        while i < self.max_tokens:
            i += 1

            predicted_token = self.predict_token(input_text + response)

            if predicted_token == "<R>":
                break
            
            predicted_token += " "
            response += predicted_token

            if predicted_token.replace(" ", "") in self.PUNCTUATION_PATTERN:
                response = response[:-3]+response[-2:]

        return response