from flask_app import app
from flask_app.controllers import patients
from flask_app.controllers import pharmacies
from flask_app.controllers import meds

if __name__ == "__main__":
    app.run(debug = True, port = '5001')
