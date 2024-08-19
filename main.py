from flask import Flask, render_template, request, jsonify
import json
from functions import save_data, load_data

app = Flask(__name__)

# %% STRONA GLOWNA      HOMEPAGE        =          http://127.0.0.1:5000/menu
@app.route("/menu")
def menu(): 
    return render_template("menu.html")


# %% DODAWANIE ZGLOSZENIA 
@app.route('/dodaj-zgloszenie')
def dodaj_zgloszenie():
    return render_template('dodaj_zgloszenie.html')


# %% New ID kod 
@app.route("/dodaj-zgloszenie2", methods = ["POST"])
def dodaj_zgloszenie2():
    
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
    # return jsonify({"message": "Task successfully added!", "task" : new_task}), 201
    return render_template("dodaj_zgloszenie.html")
    
# %% ZGLOSZENIA --> LISTA ZGLOSZEN

@app.route("/zgloszenia", methods = ["GET"])
def task_list():
    data = load_data() 
    return data
    

# %% 

    
    
# %%  TEST 1 
@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    message = request.form['message']
    
    return f'''
        <h1>Dziękujemy za przesłanie danych!</h1>
        <p><strong>Imię:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Wiek:</strong> {age}</p>
        <p><strong>Wiadomość:</strong> {message}</p>
    '''
    
    
if __name__ == "__main__":
    app.run()