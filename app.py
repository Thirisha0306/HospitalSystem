
from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1")
patients = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        illness = request.form.get("illness", "").strip()

        if name and age.isdigit() and illness:
            patients.append({
                "id": len(patients) + 1,
                "name": name,
                "age": age,
                "illness": illness
            })
        return redirect(url_for("home"))

    page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hospital System</title>
        <style>
            body { font-family: Arial; margin: 40px;
                   background: #f1f5f9; }
            .box { background: white; padding: 25px;
                   border-radius: 12px; max-width: 650px; }
            input, button { padding: 10px; margin: 6px; }
            li { margin: 12px 0; }
        </style>
    </head>
    <body>
    <div class="box">
    <h1>Hospital Management System</h1>
    <h3>Application: VERSION</h3>
    <h2>Register Patient</h2>
    <form method="POST">
        <input name="name" placeholder="Patient name" required>
        <input name="age" type="number" min="1" max="120"
               placeholder="Age" required>
        <input name="illness" placeholder="Illness" required>
        <button type="submit">Add Patient</button>
    </form>
    """

    page = page.replace("VERSION", VERSION)

    if VERSION in ("v2", "v3"):
        page += "<h2>Patient List</h2><ul>"

        for p in patients:
            page += (
                f"<li>{p['id']}. {p['name']} - "
                f"Age: {p['age']} - {p['illness']}"
            )

            if VERSION == "v3":
                page += (
                    f""" <form method="POST"
                    action="/delete/{p['id']}"
                    style="display:inline">
                    <button>Delete</button></form>"""
                )

            page += "</li>"

        page += "</ul>"

    page += "</div></body></html>"
    return page


@app.route("/delete/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):
    if VERSION != "v3":
        return "Delete is available only in v3", 404

    global patients
    patients = [p for p in patients if p["id"] != patient_id]
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy", "version": VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)