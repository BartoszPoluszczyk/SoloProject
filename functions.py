import json

def save_data(data):
    with open("zgloszenia.json", 'w', encoding='utf-8') as file:
        return json.dump(data, file, ensure_ascii=False,  indent = 4)
        
        
def load_data():
    with open("zgloszenia.json", 'r') as file:
        return json.load(file)
        