from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "trillion1122"

DATA_FILE = "data/submissions.txt"
os.makedirs("data", exist_ok=True)

submissions = []

# Load existing submissions from file on star
# Load existing submissions safely
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            parts = line.split("|")
            if len(parts) != 4:
                continue  # skip corrupted lines

            name, email, tel, message = parts
            submissions.append({
                "name": name,
                "email": email,
                "tel": tel,
                "message": message
            })

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    tel = request.form.get("tel")
    message = request.form.get("message")

    data = {
        "name": name,
        "email": email,
        "tel": tel,
        "message": message
    }

    submissions.append(data)

    # SAVE TO FILE
    with open(DATA_FILE, "a") as f:
        f.write(f"{name}|{email}|{tel}|{message}\n")

    return redirect(url_for("thank_you"))

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        return "Wrong password"
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("admin.html", submissions=submissions)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
