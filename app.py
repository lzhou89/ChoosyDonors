from flask import Flask, render_template, redirect, flash, request, session
import model
import json

app = Flask(__name__)
app.secret_key = "adfjalskdjf"
modelsession = model.session

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/portfolio_choices")
def show_portfolio_choices():
	return render_template("clusters.html")

@app.route("/confirm_portfolio")
def confirm_portfolio():
    return render_template("portfolio_confirmation.html")

@app.route("/project_search")
def search_single_project():
    query = modelsession.query(model.Project).all()
    # print query
    return render_template("single_project (copy).html", query=query)

@app.route("/project")
def show_project():
    return render_template("project_page.html")

@app.route("/keyword_search", methods=["POST"])
def keyword_search():
    print request.form.get("keyword")
    print request.form.get("zipcode")
    zip_code = request.form.get("zipcode")
    checkboxes = request.form.get("checkboxes")
    if checkboxes:
        checkboxes = checkboxes.split(",")
    print checkboxes
    look_up = modelsession.query(model.Project)
    if zip_code:
        # query = query.options(subqueryload(model.Project.school)).filter(School.zip_code==zip_code)
        query = look_up.join(model.School).filter(model.School.zip_code==zip_code)
    query = query.all()
    print query[0].id
    json_list = []
    for i in range(len(query)):
        json_list.append({"title": query[i].title, 
                        "teacher": query[i].teacher.teacher_name,
                        "school": query[i].school.school_name,
                        "location": query[i].school.city + ", " + query[i].school.state,
                        "grade": query[i].grade_level,
                        "matching": query[i].matching,
                        "keywords": "tbd",
                        "needs": query[i].fulfillment_trailer})
    results = json.dumps(json_list)
    return results

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

@app.route("/profile")
def show_profile():
    return render_template("donor_profile.html")

@app.route("/impact")
def show_impact():
    return render_template("impact.html")

#To Do:
#add donate button & check how to submit donation
#find picture
#cluster visualization
#js to enter number & show certain # of results
#ability to check to keep a project for portfolio
#confirm page remove individual projects


if __name__ == "__main__":
	app.run(debug = True)