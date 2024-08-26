from flask import Flask, render_template, request, jsonify
import json
from functions import save_data, load_data
from collections import OrderedDict

app = Flask(__name__)

# %% STRONA GLOWNA      HOMEPAGE        =          http://127.0.0.1:5000/menu
@app.route("/menu")
def menu(): 
    return render_template("menu.html")

# %% Logowanie 
@app.route('/panel-logowania')
def panel_logowania():
    return render_template("panel_logowania.html")

@app.route('/rejestracja')
def rejestracja():
    return render_template("rejsetracja.html")


# %% DODAWANIE ZGLOSZENIA 
@app.route('/dodaj-zgloszenie', methods=["GET", "POST"])
def dodaj_zgloszenie():
    if request.method == "POST":
        user = request.form.get('user')
        department = request.form.get('department')
        machine = request.form.get('machine')
        priority_level = request.form.get('priority_level')
        reporting_date = request.form.get('date')
        message = request.form.get('message')
        
        date, time = reporting_date.split("T")

        data = load_data()
        
        if data:
            max_task_id = max(int(task["task_id"]) for task in data)
            new_task_id = max_task_id + 1
        else:
            new_task_id = 1
        
        new_task = OrderedDict([    # POZWALA ZACHOWAC TAKA KOLEJNOSC JAK W PLIKU .JSON
            ('task_id', new_task_id),
            ('date', date),
            ('time', time),
            ('user', user),
            ('department', department),
            ('machine', machine),
            ('priority_level', priority_level),
            ('reporting_date', reporting_date),
            ('message', message),
        ])
        
        data.append(new_task)
        save_data(data)
        
        return render_template('success.html', new_task=new_task)

    return render_template('dodaj_zgloszenie.html')

# %% ZGLOSZENIA --> LISTA ZGLOSZEN

@app.route("/zgloszenia", methods = ["GET"])
def task_list():
    data = load_data() 
    return data
    


if __name__ == "__main__":
    app.run()