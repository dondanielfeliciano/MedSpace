from flask_app.models.patient import Patient
from flask_app.models.pharmacy import Pharmacy
from flask_app import app
from flask import redirect, render_template, session, request, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/pharmacy")
def login_registration_pharmacy():
    return render_template("pharmacy_login.html")

# @app.route("/logout")
# def log_out():
#     session.clear()
#     return render_template("login.html")

@app.route("/pharmacy_registration", methods=['POST'])
def pharmacy_registration():
    if not Pharmacy.validate_inputs(request.form):
        return redirect('/pharmacy')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'email' : request.form['email'],
        'password' : hashed_password,
        'name': request.form['name'],
        'address': request.form['address'],
        'nr': request.form['nr']
        }
    pharmacy_id = Pharmacy.save(data)
    session['pharmacy_id'] = pharmacy_id
    return redirect(f"/pharmacy_profile/{pharmacy_id}")

@app.route("/pharmacy_profile/<int:id>")
def pharmacy_profile(id):
    if 'pharmacy_id' in session and session['pharmacy_id'] == id:
        return render_template("pharmacy_profile.html", this_pharmacy = Pharmacy.get_one_pharmacy({"id": id}), pharmacy_id = session['pharmacy_id'], refills = Pharmacy.refillsRequested({'pharmacy_id':id}))
    else:
        flash('Please sign in to access your profile!','pharmacy_login')
        return redirect('/pharmacy')

@app.route("/login_pharmacy", methods=['POST'])
def login():
    one_pharmacy = Pharmacy.get_pharmacy_by_email({'email':request.form['email']})
    # print('user is', user)
    if len(one_pharmacy) == 0:
        flash('This email address is not registered. Please register first.', 'pharmacy_login')
        return redirect('/pharmacy')
    if bcrypt.check_password_hash(one_pharmacy[0]['password'],request.form['password']):
        session['pharmacy_id'] = one_pharmacy[0]['id']
        return redirect(f'pharmacy_profile/{one_pharmacy[0]["id"]}')
    else:
        flash('Incorrect password!','pharmacy_login')
        return redirect('/pharmacy')

@app.route("/pharmacy/<pharmacy_id>")
def show_one_pharmacy(pharmacy_id):
    one_pharmacy = Pharmacy.get_one_pharmacy({'id':pharmacy_id})
    return render_template("show_pharmacy.html", one_pharmacy = one_pharmacy)

@app.route("/patient_profile/<int:patient_id>/add/<int:pharmacy_id>" , methods=['POST'])
def add_pharmacy_to_patient(patient_id, pharmacy_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        print(f"the patient id is {patient_id} and the pharmacy id is {pharmacy_id}")
        Patient.add_pharmacy({"patient_id":patient_id, "pharmacy_id": pharmacy_id})
        return redirect(f"/patient_profile/{patient_id}/{pharmacy_id}")
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')
