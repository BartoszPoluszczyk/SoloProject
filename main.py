from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from functions import save_data, load_data, load_users_data, save_users_data
from collections import OrderedDict
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'CMMS'

@app.route("/test")
def test():
    return render_template('new_menu.html')
# %% STRONA GLOWNA      HOMEPAGE        =          http://127.0.0.1:5000/menu
@app.route("/menu")
def menu(): 
    return render_template("menu.html", active_page='menu')

    # return render_template("menu.html")

# %% Logowanie 
# @app.route('/panel-logowania')
# def panel_logowania():
#     return render_template("panel_logowania.html")

# %% Rejestrowanie 

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
        user_level = request.form.get ("user_level")
        
        hashed_password = generate_password_hash(password)
        data = load_users_data()
        
        #q1!11111
        
        if data:
            max_user_id = max(int(user["user_id"]) for user in data)
            user_id = max_user_id + 1
        else:
            user_id = 1
        user_email = next((user for user in data if user['email'] == email), None)
        
        if user_email:
            return jsonify({"message": "Podany email jest już zajety"}), 400
        
        # Sprawdzanie zgodności haseł
        if password != repeat_password:
            return jsonify({"message": "Niezgodność haseł"}), 400

            
        new_user = OrderedDict ([
            ('user_id' , user_id),
            ("name" , name),
            ('lastname' , lastname),
            ('email' , email.lower()),
            ('password' , hashed_password),
            ('gender', gender),
            ('regulamin1' , regulamin1),
            ('regulamin2' , regulamin2),
            ('regulamin3' , regulamin3),
            ('user_level' , user_level)
        ])

        data.append(new_user)
        save_users_data(data)
            
        return render_template("zarejestrowano.html", new_user = new_user)
    return render_template("rejestracja.html")

# %% Logowanie 
@app.route("/panel-logowania", methods = ["GET", "POST"])
def panel_logowania():
    data = load_users_data()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = next((user for user in data if user['email'] == email), None)
    
        if user:
            print("Hash zapisany w systemie:", user['password'])
            print("Hasło podane przez użytkownika:", password)
            if check_password_hash(user['password'], password):
                session['email'] = user['email']
                session['user_id'] = user['user_id']
                session['name'] = user['name']
                session['lastname'] = user['lastname']
                session['user_level'] = user['user_level']
                session.permanent = True
                session.permanent_session_lifetime = timedelta(minutes=30) 
                return redirect(url_for('menu'))
                # return render_template("menu.html")
            else:
                return jsonify({"message": "Bledne dane logowania"})
        else:
            return jsonify({"message": f"Brak uzytkownika o podanym emailu {email}"})
            
       
    return render_template("panel_logowania.html")


# %% Wylogowanie sesji
@app.route("/wylogowanie", methods=['GET', 'POST'])
def wylogowanie():
    session.pop('email', None)
    session.pop('user_id', None)
    return redirect(url_for('panel_logowania'))

# %% DODAWANIE ZGLOSZENIA 
@app.route('/dodaj-zgloszenie', methods=["GET", "POST"])
def dodaj_zgloszenie():
    if 'email' in session:
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
    else:
        return redirect(url_for('panel_logowania'))

# %% ZGLOSZENIA --> LISTA ZGLOSZEN
@app.route('/zgloszenia')
def zgloszenia():
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')
    
    if 'email' in session:
        try:
            data = load_data()  # Ładowanie zgłoszeń z pliku zgloszenia.json
            if sort_by == 'machine':
                sorted_data = sorted(zgloszenia, key = lambda x:x['machine'], reverse = (order == 'desc'))
            elif sort_by == 'department':
                sorted_data = sorted(zgloszenia, key = lambda x:x['department'], reverse = (order == 'desc'))
            else:
                sorted_data = zgloszenia
            return render_template('zgloszenia.html', zgloszenia=data, sorted_zgloszenia = sorted_data, active_page='zgloszenia')
        except Exception as e:
            return 'Error loading data: ' + str(e)
    else:
        return redirect(url_for('panel_logowania'))
    
# %% Szczegoly zgloszenia
@app.route('/zgloszenie/<int:task_id>')
def zgloszenie_szczegoly(task_id):
    if 'email' in session:
        data = load_data()
        zgloszenie = next((item for item in data if item['task_id'] == task_id), None)
        if zgloszenie:
            return render_template('zgloszenie_szczegoly.html', zgloszenie=zgloszenie)
        else:
            return "Zgłoszenie nie znalezione", 404
    else:
        return redirect(url_for('panel_logowania'))
    
# %% Edycja zgloszenia 
@app.route('/zgloszenie/<int:task_id>/edit', methods=["PATCH, PUT"])
def zgloszenie_edycja(task_id):
    # Tu wyświetl formularz do edycji zgłoszenia
    zgloszenie = next((z for z in zgloszenia if z['task_id'] == task_id), None)
    return render_template('zgloszenie_edycja.html', zgloszenie=zgloszenie)


@app.route('/zgloszenie-usun')
def zgloszenie_usun():
    return render_template('menu.html')


# %% Zakladki do zagospodarowania 

@app.route('/urzadzenia')
def urzadzenia():
    return render_template("urzadzenia.html", active_page='urzadzenia')
    
    
    
@app.route('/przeglady')
def przeglady():
    return render_template('przeglady.html', active_page='przeglady')

@app.route('/raport')
def raport():
    return render_template('raport.html', active_page='raport')

@app.route('/statystyka')
def statystyka():
    return render_template('statystyka.html', active_page='statystyka')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html', active_page='kontakt')










if __name__ == "__main__":
    app.run(debug=True)
    
    