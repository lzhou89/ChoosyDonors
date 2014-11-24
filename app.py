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

@app.route("/portfolio_projects")
def select_portfolio_projects():
    query = modelsession.query(model.Project).all()
    return render_template("portfolio_selection.html", query=query)

@app.route("/mid_portfolio", methods=["POST"])
def save_portfolio_projects():
    checkboxes = request.form.get("checkboxes")
    if checkboxes:
        checkboxes = checkboxes.split(",")
        if "portfolio" not in session:
            session["portfolio"] = []
        for item in checkboxes:
            session["portfolio"].append(item)
    return redirect("/confirm_portfolio")

@app.route("/confirm_portfolio")
def confirm_portfolio():
    saved_projects = session["portfolio"]
    projects = []
    for item in saved_projects:
        query = modelsession.query(model.Project).get(item)
        projects.append(query)
    return render_template("portfolio_confirmation.html", query=projects)

@app.route("/project_search")
def search_single_project():
    checkboxes = {}
    subjects = {}
    areas = modelsession.query(model.ProjSub).distinct(model.ProjSub.subject).all()
    for row in areas:
        if row.focus_area in subjects:
            if row.subject not in subjects[row.focus_area]:
                subjects[row.focus_area].append(row.subject)
        else:
            subjects[row.focus_area] = [row.subject]
    checkboxes["Subjects"] = subjects
    resources = modelsession.query(model.Project.resource_type).distinct(model.Project.resource_type).all()
    for item in resources:
        if "Resources" in checkboxes:
            checkboxes["Resources"].append(item[0])
        else:
            checkboxes["Resources"] = [item[0]]
    grades = modelsession.query(model.Project.grade_level).distinct(model.Project.grade_level).all()
    for grade in grades:
        if "Grades" in checkboxes:
            checkboxes["Grades"].append(grade[0])
        else:
            checkboxes["Grades"] = [grade[0]]
    # sort_grades = sorted(checkboxes["Grades"])
    query = modelsession.query(model.Project).all()
    print query[0].id
    area_list = subjects.keys()
    # print query
    return render_template("single_project (copy).html", query=query, menu = checkboxes, areas = area_list)

@app.route("/project/<project_id>")
def show_project(project_id):
    # project_id = '"'+project_id+'"'
    project = modelsession.query(model.Project).get(project_id)
    return render_template("project_page.html", project=project)

@app.route("/keyword_search", methods=["POST"])
def keyword_search():
    categories = generate_dict()
    print categories
    print request.form.get("keyword")
    print request.form.get("zipcode")
    zip_code = request.form.get("zipcode")
    checkboxes = request.form.get("checkboxes")
    query = modelsession.query(model.Project)
    if zip_code:
        print "ok"
        # query = query.options(subqueryload(model.Project.school)).filter(School.zip_code==zip_code)
        query = query.join(model.School).filter(model.School.zip_code==zip_code)
    if checkboxes:
        checkboxes = checkboxes.split(",")
        for item in checkboxes:
            print item
            item = item.encode("utf-8")
            category = categories[item]
            print category
            if category == "subject":
                query = query.join(model.ProjSub).filter(model.ProjSub.subject==item)
            if category == "area":
                query = query.join(model.ProjSub).filter(model.ProjSub.focus_area==item)
            if category == "resource":
                query = query.filter(model.Project.resource_type==item)
            if category == "grade":
                query = query.filter(model.Project.grade_level==item)
    print checkboxes
    
    query = query.all()
    # print query
    # print query[0].id
    json_list = []
    for i in range(len(query)):
        json_list.append({"id": query[i].id,
                        "title": query[i].title, 
                        "teacher": query[i].teacher.teacher_name,
                        "school": query[i].school.school_name,
                        "location": query[i].school.city + ", " + query[i].school.state,
                        "grade": query[i].grade_level,
                        "matching": query[i].matching,
                        "keywords": "tbd",
                        "needs": query[i].fulfillment_trailer})
    results = json.dumps(json_list)
    return results

def generate_dict():
    categories = {}
    subjects = modelsession.query(model.ProjSub.subject).distinct(model.ProjSub.subject).all()
    for item in subjects:
        categories[item[0].encode("utf-8")] = "subject"
    areas = modelsession.query(model.ProjSub.focus_area).distinct(model.ProjSub.focus_area).all()
    for item in areas:
        categories[item[0].encode("utf-8")] = "area"
    resources = modelsession.query(model.Project.resource_type).distinct(model.Project.resource_type).all()
    for item in resources:
        categories[item[0].encode("utf-8")] = "resource"
    grades = modelsession.query(model.Project.grade_level).distinct(model.Project.grade_level).all()
    for item in grades:
        categories[item[0].encode("utf-8")] = "grade"
    return categories

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
#cluster visualization
#js to enter number & show certain # of results
#ability to check to keep a project for portfolio - add checked to session
#confirm page remove individual projects - delete from session
#search doesn't combine subjects, only adds them so AND instead of OR


if __name__ == "__main__":
	app.run(debug = True)