from flask_app.models.patient import Patient
from flask_app.models.pharmacy import Pharmacy
from flask_app.models.med import Med
from flask_app import app
from flask import redirect, render_template, session, request, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def welcome_page():
    return render_template("welcome.html")

@app.route("/patients")
def login_registration_patient():
    return render_template("patient_login.html")

@app.route("/logout")
def log_out():
    session.clear()
    return render_template("welcome.html")

@app.route("/patient_registration", methods=['POST'])
def patient_registration():
    if not Patient.validate_inputs(request.form):
        return redirect('/patients')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'email' : request.form['email'],
        'password' : hashed_password,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'bdate': request.form['bdate'],
        'address': request.form['address']
        }
    patient_id = Patient.registration(data)
    session['patient_id'] = patient_id
    return redirect(f"/patient_profile/{patient_id}")

@app.route("/patient_profile/<int:id>")
def patient_profile(id):
    if 'patient_id' in session and session['patient_id'] == id:
        return render_template("patient_profile.html", one_patient = Patient.get_one_patient({"id": id}), all_unselected_pharmacies = Pharmacy.get_all_unselected_pharmacies({"id":id}), patient_id = session['patient_id'], pharmacies_added = Pharmacy.pharmacies_added({"id":id}), all_medications = Med.get_all_meds_one_patient({"id":id}))
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route("/patient_profile/<int:id>/pharmacies")
def patient_profile_pharmacies(id):
    if 'patient_id' in session and session['patient_id'] == id:
        return render_template("patient_profile_pharmacies.html", one_patient = Patient.get_one_patient({"id": id}), all_unselected_pharmacies = Pharmacy.get_all_unselected_pharmacies({"id":id}), patient_id = session['patient_id'], pharmacies_added = Pharmacy.pharmacies_added({"id":id}), all_medications = Med.get_all_meds_one_patient({"id":id}))
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route("/login_patient", methods=['POST'])
def login_patient():
    patient = Patient.get_patient_by_email({'email':request.form['email']})
    if len(patient) == 0:
        flash('This email address is not registered. Please register first.', 'patient_login')
        return redirect('/patients')
    if bcrypt.check_password_hash(patient[0]['password'],request.form['password']):
        session['patient_id'] = patient[0]['id']
        return redirect(f'patient_profile/{patient[0]["id"]}')
    else:
        flash('Incorrect password!','patient_login')
        return redirect('/patients')

@app.route('/remove_pharmacy/<int:patient_id>/<int:pharmacy_id>')
def removePatientPharmacy(patient_id, pharmacy_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        data ={
            'patient_id': patient_id,
            'pharmacy_id': pharmacy_id
        }
        Patient.removePharmacy(data)
        return redirect(f'/patient_profile/{patient_id}')
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

