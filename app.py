from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "diettracker123"  

users = []

@app.route("/")
def welcome():
    return render_template("welcome.html")

# Intro Page 
@app.route("/intro")
def intro():
    return render_template("intro.html")

# Register Page
@app.route("/register")
def register():
    return render_template("register.html")

# Save User
@app.route("/save_user", methods=["POST"])
def save_user():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    weight = request.form["weight"]
    height = request.form["height"]
    goal = request.form["goal"]

    # check duplicate user
    for user in users:
        if user["email"] == email:
            return redirect(url_for("login", msg="already"))

    user = {
        "name": name,
        "email": email,
        "password": password,
        "age": age,
        "weight": weight,
        "height": height,
        "goal": goal
    }

    users.append(user)

    return redirect(url_for("login",
                msg="Registration Successful ✔ Please Login"))

# Login Page
@app.route("/login")
def login():
    msg = request.args.get("msg")
    # return render_template("login.html", msg=msg)
    if len(users) == 0:
        return render_template("login.html", msg="register_first")

    return render_template("login.html", msg=msg)

# Check Login

@app.route("/check_login", methods=["POST"])
def check_login():

    email = request.form["email"]
    password = request.form["password"]

    #  No users
    if len(users) == 0:
        return redirect(url_for("login", msg="Kindly register first ❗"))

    for user in users:
        if user["email"] == email:
            if user["password"] == password:
                session["user"] = email
                return redirect(url_for("meal"))
            else:
                return redirect(url_for("login", msg="Wrong password ❗"))

    return redirect(url_for("login", msg="User not found ❗ Please register"))
# Meal Dashboard
@app.route("/meal")
def meal():

    #  LOGIN SECURITY
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("meal.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)