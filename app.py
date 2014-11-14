from flask import Flask, render_template, redirect, flash, request, session
import model

app = Flask(__name__)
app.secret_key = "adfjalskdjf"
modelsession = model.session

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/portfolio_choices")
def show_portfolio_choices():
	return render_template("clusters.html")

@app.route("/login", methods=["GET"])
def show_login():
    if "user_id" in session:
        del session["user_id"]
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    # password = request.form.get("password")

    user = modelsession.query(model.Donor).filter_by(email = email).first()

    if user:
         session["user_id"] = user.id
         flash("Successfully logged in")
         return redirect ("/")
    else:
         flash("Username not found")
         return redirect("/login") 

if __name__ == "__main__":
	app.run(debug = True)