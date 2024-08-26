from flask import Flask, request, render_template

app = Flask(__name__)

# %% Logowanie do aplikacji 

@app.route('/panel-logowania')
def panel_logowania():
    return render_template("logowanie.hrml")






'''
    user_name = request.form.get("user_name")
    password = request.form.get("password")

    dane_logowania = {
        "user_name": user_name,
        "password": password
        }
'''






















if __name__ == "__main__":
    app.run()

