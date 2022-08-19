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
        return render_template("pharmacy_profile.html", this_pharmacy = Pharmacy.get_one_pharmacy({"id": id}), pharmacy_id = session['pharmacy_id'])
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

# @app.route("/purchases/<int:user_id>")
# def display_purchases(user_id):
#     user_with_purchased_cars = User.get_bought_cars({'id':user_id})
#     # print("here's the profile holder's info plus purchased cars",user_with_purchased_cars)
#     return render_template("purchases.html", user = user_with_purchased_cars)

