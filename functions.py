import json

# %% Lista zgloszen 
def save_data(data):
    with open("zgloszenia.json", 'w', encoding='utf-8') as file:
        return json.dump(data, file, ensure_ascii=False,  indent = 4)
        
def load_data():
    with open("zgloszenia.json", 'r') as file:
        return json.load(file)
        
        
# %% Dane logowania

def load_users_data():
    with open("users_data.json" , 'r')as file:
        return json.load(file)
    
def save_users_data(data):
    with open("users_data.json", 'w', encoding = "utf-8") as file:
        return json.dump(data, file, ensure_ascii = False, indent = 4)
    
def load_device_data():
    with open('devices.json', 'r') as file:
        return json.load(file)
    
def save_device_data(data):
    with open('devices.json', 'w', encoding = "utf-8") as file:
        return json.dump(data, file, ensure_ascii=False, indent = 4)
        