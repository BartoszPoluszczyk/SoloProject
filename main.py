from flask import Flask, render_template, request, jsonify
import json
from functions import save_data, load_data, load_users_data, save_users_data
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

@app.route('/rejestracja', methods = ["GET", "POST"])
def rejestracja():
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        gender = request.form.get("gender")
        regulamin1 = request.form.get("regulamin1")
        regulamin2 = request.form.get("regulamin2")
        regulamin3 = request.form.get("regulamin3")
        
        data = load_users_data()
        
        if data:
            max_user_id = max(int(user["user_id"]) for user in data)
            user_id = max_user_id + 1
        else:
            user_id = 1
        
        if password != repeat_password:
            return jsonify({"message": "Niezgodnosc hasel"}), 400

        else:
            new_user = OrderedDict ([
                ('user_id' , user_id),
                ("name" , name),
                ('lastname' , lastname),
                ('email' , email.lower()),
                ('password' , password),
                ('gender' , gender)
            ])
    
            data.append(new_user)
            save_users_data(data)
            
        return render_template("zarejestrowano.html", new_user = new_user)
    return render_template("rejestracja.html")


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