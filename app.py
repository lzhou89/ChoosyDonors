from flask import Flask, render_template, redirect, flash, request, session, url_for
from sqlalchemy import func
import model
import json
import string

app = Flask(__name__)
app.secret_key = "adfjalskdjf"
modelsession = model.session

@app.route("/")
def index():
    """This is the 'cover' page of ChoosyDonors."""
    return render_template("index.html")

@app.route("/portfolio_choices")
def show_portfolio_choices():
    """This page presents the available clusters in a word cloud."""
    return render_template("clusters.html")

@app.route("/portfolio_projects/<id>")
def select_portfolio_projects(id):
    """This page allows users to choose n random projects in the cluster."""
    cluster_id = id
    return render_template("portfolio_selection.html", id=cluster_id)

@app.route("/load_projects", methods=["POST"])
def load_projects():
    """Takes 'n' the user specifies and returns n projects from the cluster."""
    number = request.form.get("number")
    print number
    cluster_id = request.form.get("id")
    print cluster_id
    #returns n random projects in chosen cluster
    cluster_query = modelsession.query(model.Cluster).filter(
                    model.Cluster.cluster_num==cluster_id).order_by(
                    func.random()).limit(number).all()
    print len(cluster_query)
    projects = []
    #loops through projects in cluster_query to create a list of the project objs.
    for item in cluster_query:
        proj_id = item.project_id
        proj_id = '"'+proj_id+'"'
        print proj_id
        query = modelsession.query(model.Project).filter(
                model.Project.id==proj_id).first()
        projects.append(query)
    print projects
    #creates a json object to pass to javascript
    json_list = []
    for i in range(len(projects)):
        json_list.append({"id": projects[i].id,
                        "title": projects[i].title, 
                        "location": projects[i].school.city + ", " + 
                                    projects[i].school.state,
                        "grade": projects[i].grade_level,
                        "needs": projects[i].fulfillment_trailer})
    results = json.dumps(json_list)
    return results

@app.route("/mid_portfolio", methods=["POST"])
def save_portfolio_projects():
    """Saves the projects chosen for the portfolio to the session."""
    checkboxes = request.form.get("checkboxes")
    if checkboxes:
        checkboxes = checkboxes.split(",")
        print checkboxes
        if "portfolio" not in session:
            session["portfolio"] = []
        for item in checkboxes:
            session["portfolio"].append(item)
        print session["portfolio"]
    return "/confirm_portfolio"

@app.route("/confirm_portfolio")
def confirm_portfolio():
    """This page shows the projects selected for the portfolio."""
    saved_projects = session["portfolio"]
    projects = []
    for item in saved_projects:
        item = '"'+item+'"'
        query = modelsession.query(model.Project).get(item)
        projects.append(query)
    return render_template("portfolio_confirmation.html", query=projects)

@app.route("/clear_all", methods=["GET"])
def clear_portfolio():
    """Removes all projects from portfolio."""
    session["portfolio"] = []
    return "ok"

@app.route("/clear_selected", methods=["POST"])
def clear_project():
    """Removes selected projects from portfolio."""
    checkboxes = request.form.get("checkboxes")
    checkboxes = checkboxes.split(",")
    checkboxes = [project[1:-1] for project in checkboxes]
    print checkboxes
    saved_projects = session["portfolio"]
    print saved_projects
    new_project_list = [project for project in saved_projects 
                        if project not in checkboxes]
    print new_project_list
    session["portfolio"] = new_project_list
    return "ok"

@app.route("/save_portfolio", methods=["POST"])
def save_portfolio():
    """Saves portfolio to database."""
    name = request.form.get("portfolio_name")
    print name
    print session["portfolio"]
    print session["user_id"]
    for item in session["portfolio"]:
        pid = '"'+item+'"'
        p = model.Portfolio()
        p.donor_id = session["user_id"]
        p.project_id = pid
        p.portfolio_title = name
        modelsession.add(p)
    modelsession.commit()
    session["portfolio"] = []
    flash("Portfolio successfully saved")
    return redirect("/confirm_portfolio")


@app.route("/project_search")
def search_single_project():
    """This page allows categorical search of projects."""
    checkboxes = {}
    subjects = {}
    # commented out code is a different implementation that I want to optimize
    # areas = modelsession.query(model.ProjSub).distinct(
        # model.ProjSub.subject).all()
    # for row in areas:
    #     if row.focus_area in subjects:
    #         if row.subject not in subjects[row.focus_area]:
    #             subjects[row.focus_area].append(row.subject)
    #     else:
    #         subjects[row.focus_area] = [row.subject]
    areas = ["Math & Science", "Music & The Arts", "Literacy & Language", 
    "History & Civics", "Special Needs", "Applied Learning", "Health & Sports"]
    ms_subjects = ["Environmental Science", "Mathematics", "Health & Life Science", 
    "Applied Sciences"]
    ma_subjects = ["Performing Arts", "Visual Arts", "Music"]
    ll_subjects = ["Literacy", "Literature & Writing", "Foreign Languages", "ESL"]
    his_subjects = ["History & Geography", "Civics & Government", "Economics", 
    "Social Sciences"]
    al_subjects = ["Early Development", "Community Service", "Character Education", 
    "College & Career Prep", "Extracurricular", "Parent Involvement", "Other"]
    hea_subjects = ["Sports", "Health & Wellness", "Nutrition", "Gym & Fitness"]
    area_subs = [ms_subjects, ma_subjects, ll_subjects, his_subjects, [], 
    al_subjects, hea_subjects]

    for i in range(len(areas)):
        subjects[areas[i]] = area_subs[i]

    checkboxes["Subjects"] = subjects
    # resources = modelsession.query(model.Project.resource_type).distinct(
        # model.Project.resource_type).all()
    # for item in resources:
    #     if "Resources" in checkboxes:
    #         checkboxes["Resources"].append(item[0])
    #     else:
    #         checkboxes["Resources"] = [item[0]]
    resources = ["Books", "Technology", "Supplies", "Trips", "Visitors", "Other"]
    checkboxes["Resources"] = resources
    # grades = modelsession.query(model.Project.grade_level).distinct(
        # model.Project.grade_level).all()
    # for grade in grades:
    #     if "Grades" in checkboxes:
    #         checkboxes["Grades"].append(grade[0])
    #     else:
    #         checkboxes["Grades"] = [grade[0]]
    # sort_grades = sorted(checkboxes["Grades"])
    grades = ["Grades PreK-2", "Grades 3-5", "Grades 6-8", "Grades 9-12"]
    checkboxes["Grades"] = grades
    # query = modelsession.query(model.Project).all()
    query = modelsession.query(model.Project).limit(100)
    needs = []
    for item in query:
        need = item.fulfillment_trailer
        need = need.split(", including")[0]
        needs.append(need)
    # area_list = subjects.keys()
    # return render_template("single_project.html", query=query, 
                            # menu = checkboxes, areas = area_list)
    return render_template("single_project.html", query=query, menu=checkboxes, 
                            areas=areas, needs=needs)
    
@app.route("/project/<project_id>")
def show_project(project_id):
    """This page shows all information for the project."""
    project = modelsession.query(model.Project).get(project_id)
    description = str(project.synopsis)
    description = string.replace(description, "\\n", "\n")
    needs = str(project.fulfillment_trailer)
    needs = needs.split(", including")[0]
    print needs
    return render_template("project_page.html", project=project, 
                            description=description, needs=needs)

@app.route("/keyword_search", methods=["POST"])
def keyword_search():
    """Performs categorical search."""
    categories = generate_dict()
    print categories
    print request.form.get("zipcode")
    zip_code = request.form.get("zipcode")
    checkboxes = request.form.get("checkboxes")
    query = modelsession.query(model.Project)
    if zip_code:
        query = query.join(model.School).filter(model.School.zip_code==zip_code)
    if checkboxes:
        checkboxes = checkboxes.split(",")
        for item in checkboxes:
            print item
            item = item.encode("utf-8")
            category = categories[item]
            print category
            if category == "subject":
                query = query.join(model.ProjSub).filter(
                        model.ProjSub.subject==item)
            if category == "area":
                query = query.join(model.ProjSub).filter(
                        model.ProjSub.focus_area==item)
            if category == "resource":
                query = query.filter(model.Project.resource_type==item)
            if category == "grade":
                query = query.filter(model.Project.grade_level==item)
    print checkboxes
    
    # query = query.all()
    query = query.limit(100).all()
    print query[0].id
    #creates a json object to pass to javascript
    json_list = []
    for i in range(len(query)):
        json_list.append({"id": query[i].id,
                        "title": query[i].title, 
                        "location": query[i].school.city + ", " + 
                                    query[i].school.state,
                        "grade": query[i].grade_level,
                        "needs": query[i].fulfillment_trailer})
    results = json.dumps(json_list)
    return results

def generate_dict():
    """Creates a dictionary of menu items to create search accordion menu."""
    #commented out code is a different implementation I want to optimize
    print "start dict"
    categories = {}
    subjects =["Environmental Science", "Mathematics", "Health & Life Science", 
                "Applied Sciences", "Performing Arts", "Visual Arts", "Music", 
                "Literacy", "Literature & Writing", "Foreign Languages", "ESL", 
                "History & Geography", "Civics & Government", "Economics", 
                "Social Sciences", "Early Development", "Community Service", 
                "Character Education", "College & Career Prep", "Extracurricular", 
                "Parent Involvement", "Other", "Sports", "Health & Wellness", 
                "Nutrition", "Gym & Fitness"]
    for item in subjects:
        categories[item] = "subject"
    # subjects = modelsession.query(model.ProjSub.subject).distinct(
                # model.ProjSub.subject).all()
    # for item in subjects:
    #     categories[item[0].encode("utf-8")] = "subject"
    areas = ["Math & Science", "Music & The Arts", "Literacy & Language", 
            "History & Civics", "Special Needs", "Applied Learning", 
            "Health & Sports"]
    for item in areas:
        categories[item] = "area"
    # areas = modelsession.query(model.ProjSub.focus_area).distinct(
            # model.ProjSub.focus_area).all()
    # for item in areas:
    #     categories[item[0].encode("utf-8")] = "area"
    resources = ["Books", "Technology", "Supplies", "Trips", "Visitors", "Other"]
    for item in resources:
        categories[item] = "resource"
    # resources = modelsession.query(model.Project.resource_type).distinct(
                # model.Project.resource_type).all()
    # for item in resources:
    #     categories[item[0].encode("utf-8")] = "resource"
    grades = ["Grades PreK-2", "Grades 3-5", "Grades 6-8", "Grades 9-12"]
    for item in grades:
        categories[item] = "grade"
    # grades = modelsession.query(model.Project.grade_level).distinct(
            # model.Project.grade_level).all()
    # for item in grades:
    #     categories[item[0].encode("utf-8")] = "grade"
    return categories

@app.route("/login", methods=["GET"])
def show_login():
    """This is the login page."""
    if "user_id" in session:
        del session["user_id"]
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """This verifies a user's username & password."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = modelsession.query(model.Donor).filter_by(email=email).first()

    if user and user.password == password:
         session["user_id"] = user.id
         flash("Successfully logged in")
         return redirect ("/")
    elif user and user.password != password:
        flash("Incorrect password")
        return redirect("/login")
    else:
         flash("Username not found")
         return redirect("/login") 

@app.route("/profile/<donor_id>")
def show_profile(donor_id):
    """This page shows a donor's information."""
    donor = modelsession.query(model.Donor).get(donor_id)
    #creates a dictionary of donor's portfolios
    portfolios = {}
    for item in donor.portfolios:
        query = modelsession.query(model.Project).get(item.project_id)
        if item.portfolio_title in portfolios:
            portfolios[item.portfolio_title].append((query.id, query.title))
        else:
            portfolios[item.portfolio_title] = [(query.id, query.title)]
    print portfolios
    return render_template("donor_profile.html", donor=donor, 
                            portfolios=portfolios)

@app.route("/impact")
def show_impact():
    """This page shows d3 map of impact scores & projects."""
    url_for('static', filename='zips_us_topo.json')
    url_for('static', filename='pov_levels.csv')
    query = modelsession.query(model.Project).order_by(func.random()).limit(1000).all()
    #creates a json object to be passed to javascript
    json_list = []
    for i in range(len(query)):
        json_list.append({"id": query[i].id,
                        "title": query[i].title, 
                        "latitude": query[i].school.latitude,
                        "longitude": query[i].school.longitude,
                        "location": query[i].school.city + ", " + query[i].school.state,
                        "grade": query[i].grade_level,
                        "needs": query[i].fulfillment_trailer})
    results = json.dumps(json_list)
    print "results sending"
    return render_template("impact.html", results=results)


if __name__ == "__main__":
    app.run(debug = True)
    
