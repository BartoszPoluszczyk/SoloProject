import json

def save_data(data):
    with open("zgloszenia.json", 'w') as file:
        return json.dump(data, file, indent = 4)
        
        
def load_data():
    with open("zgloszenia.json", 'r') as file:
        return json.load(file)
        