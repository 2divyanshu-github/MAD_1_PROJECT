from flask import Flask, render_template, redirect, request
from flask import current_app as app #if you directly import app> circular 
#current _app refers to app object that we created. 
from .models import *
# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use("Agg")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username, password=pwd).first() #LHS> table attribute , rhs>form data 
        
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    return render_template("admin_dash.html",this_user=this_user)
                else:
                    return render_template("user_dash.html",this_user=this_user)
                # Here we can add logic to check username and password
            else:
                return "Invalid password"
        else:
            return "User not found"
        
    return render_template("login.html")


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_name or user_email:
            return "Username already exists"
        else:
            user = User(username=username, email=email, password=pwd)
            db.session.add(user)
            db.session.commit()
            # After registering, we can redirect to login page or show a success message
        return "Registered successfully"
    return render_template("register.html")



# @app.route('/add-ebook', methods=['POST'])
# @login_required # ✅ Ensures user is logged in
# def add_ebook():
#     # ✅ Check if the user is an admin
#     if not current_user.is_admin:
#         abort(403)  # Forbidden

#     # ✅ Get form data
#     name = request.form.get('name')
#     author = request.form.get('author')
#     url = request.form.get('url')

#     # ✅ Validate required fields
#     if not name or not author or not url:
#         return "Missing fields", 400

#     # ✅ Create and save the ebook with current_user.id
#     new_ebook = Ebook(
#         name=name,
#         author=author,
#         url=url,
#         user_id=current_user.id
#     )

#     db.session.add(new_ebook)
#     db.session.commit()

#     return redirect(url_for('your_success_page'))  # Or return a message


# # -------------------------------------------------------------------------------------------------------------------------------

# from flask import request, redirect, url_for
# from flask_login import login_required, current_user
# from app import app, db  # Replace `yourapp` with your app's name
# from application.models import Ebook  # Adjust import path

# # # ✅ Route to handle ebook creation
# # @app.route("/create_ebook", methods=['POST'])
# # @login_required  # ✅ Ensures user is logged in
# @app.route("/create_ebook", methods=["GET", "POST"])
# def add_ebook():
#     # ✅ Get form data from request
#     name = request.form.get('name')
#     author = request.form.get('author')
#     url = request.form.get('url')

#     # ✅ Make sure all required fields are present
#     if not name or not author or not url:
#         return "Missing required fields", 400

#     # ✅ This is the key part: use current_user.id to prevent user_id=None
#     new_ebook = Ebook(
#         name=name,
#         author=author,
#         url=url,
#         user_id=current_user.id  # ✅ This prevents the IntegrityError
#     )

#     # ✅ Add and commit to the database
#     db.session.add(new_ebook)
#     db.session.commit()

#     return redirect(url_for('your_success_page'))  # or return a success message


# --------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/create_ebook", methods=["GET", "POST"])
def create():
  this_user= User.query.filter_by(type="admin").first()
  if request.method == "POST":
    name= request.form.get("name")
    author = request.form.get("author")
    url = request.form.get("url")
    ebook = Ebook(name=name, author=author,url=url)
    db.session.add(ebook)
    db.session.commit()
    return redirect("/admin")
  return render_template("create_ebook.html")



@app.route("/request-ebook/<int:user_id>")
def request_ebook(user_id):
    this_user = User.query.filter_by(id=user_id).first()
    ebooks = Ebook.query.filter_by(status="available").all()
    return render_template("request.html", this_user=this_user, ebooks=ebooks)