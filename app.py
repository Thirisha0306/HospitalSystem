from flask import Flask, request, redirect, url_for

app = Flask(__name__)

patients = []


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age")
        illness = request.form.get("illness")

        patient = {
            "id": len(patients) + 1,
            "name": name,
            "age": age,
            "illness": illness
        }

        patients.append(patient)

        return redirect(url_for("home"))

    html = """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Hospital Management System - V3</title>

        <style>

            body {
                font-family: Arial;
                background: #f2f2f2;
                margin: 40px;
            }

            .container {
                background: white;
                padding: 30px;
                max-width: 900px;
                margin: auto;
                border-radius: 10px;
            }

            input {
                padding: 10px;
                margin: 5px;
            }

            button {
                padding: 10px 20px;
                cursor: pointer;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 25px;
            }

            th, td {
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }

            th {
                background: #eee;
            }

            .delete-button {
                background: #dc3545;
                color: white;
                border: none;
                padding: 8px 12px;
            }

        </style>

    </head>

    <body>

    <div class="container">

        <h1>Hospital Management System</h1>

        <h2>Version 3 - Delete Patient</h2>

        <h3>Register Patient</h3>

        <form method="POST">

            <input
                type="text"
                name="name"
                placeholder="Patient Name"
                required
            >

            <input
                type="number"
                name="age"
                placeholder="Age"
                required
            >

            <input
                type="text"
                name="illness"
                placeholder="Illness"
                required
            >

            <button type="submit">
                Add Patient
            </button>

        </form>

        <h3>Patient List</h3>

        <table>

            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>Illness</th>
                <th>Action</th>
            </tr>
    """

    for patient in patients:

        html += f"""

            <tr>

                <td>{patient['id']}</td>

                <td>{patient['name']}</td>

                <td>{patient['age']}</td>

                <td>{patient['illness']}</td>

                <td>

                    <form
                        method="POST"
                        action="/delete/{patient['id']}"
                    >

                        <button
                            class="delete-button"
                            type="submit"
                        >
                            Delete
                        </button>

                    </form>

                </td>

            </tr>

        """

    html += """

        </table>

    </div>

    </body>

    </html>

    """

    return html


@app.route("/delete/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):

    global patients

    patients = [
        patient
        for patient in patients
        if patient["id"] != patient_id
    ]

    return redirect(url_for("home"))


@app.route("/health")
def health():

    return {
        "status": "healthy",
        "version": "v3"
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )