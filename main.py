from flask import Flask, render_template 

app = Flask(__name__)

# %% STRONA GLOWNA
@app.route("/menu")
def menu(): 
    return render_template("menu.html")


# %% DODAWANIE ZGLOSZENIA 
@app.route("/dodaj-zgloszenie", methods = ["POST"])
def dodaj_zgloszenie():
    pass


if __name__ == "__main__":
    app.run()
# %%
