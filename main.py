from flask import Flask, render_template, request, jsonify
import json
from functions import save_data, load_data

app = Flask(__name__)

# %% STRONA GLOWNA      HOMEPAGE        =          http://127.0.0.1:5000/menu
@app.route("/menu")
def menu(): 
    return render_template("menu.html")


# %% DODAWANIE ZGLOSZENIA 
@app.route("/dodaj-zgloszenie", methods = ["POST"])
def dodaj_zgloszenie():
    
    if request.json:
        new_task = request.json
    else:
        return jsonify({"message": "No input provided"}), 400
    
    data = load_data()
    new_task_id = []
    
    if data:
        max_task_id = max(int(task["task_id"]) for task in data)
        new_task_id = max_task_id + 1
    else:
        new_task_id = 1
    new_task['task_id'] = new_task_id
    
    
    data.append(new_task)
    save_data(data)
    return jsonify({"message": "Task successfully added!", "task" : new_task}), 201
    
# %% ZGLOSZENIA --> LISTA ZGLOSZEN

@app.route("/zgloszenia", methods = ["GET"])
def task_list():
    data = load_data() 
    return data
    

# %% 
if __name__ == "__main__":
    app.run()
    
    
# %%
