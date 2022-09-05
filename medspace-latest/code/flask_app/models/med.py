from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app import app
from flask_app.models import pharmacy
from flask_app.models import patient
from flask import flash, session

db='medspace'

class Med:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.directions = data['directions']
        self.days_left = data['days_left']
        self.refills = data['refills']
        self.patient_id = session['patient_id']
        self.pharmacy_id = data['pharmacy_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.refill_request = data['refill_request']
        self.patient = None
        self.pharmacy = None

    @classmethod
    def save(cls,data):
        query = 'insert into medications (name, directions, days_left, refills, patient_id, pharmacy_id, refill_request) values (%(name)s, %(directions)s, %(days_left)s, %(refills)s, %(patient_id)s, %(pharmacy_id)s, %(refill_request)s)'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_one_med(cls, data):
        query = 'select * from medications where id = %(id)s'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_meds_one_patient_one_pharmacy(cls, data):
        query = 'select * from medications where patient_id = %(patient_id)s and pharmacy_id = %(pharmacy_id)s'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_meds_one_patient(cls, data):
        query = 'select * from medications join pharmacies on medications.pharmacy_id = pharmacies.id where patient_id = %(id)s'
        results = connectToMySQL(db).query_db(query, data)
        return results

    # @classmethod
    # def delete_med(cls,data):
    #     query = 'delete from medications where id = %(med_id)s'
    #     return connectToMySQL(db).query_db(query, data)


    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM medications WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def requestRefill(cls,data):
        query = 'UPDATE medications SET refill_request = 1 WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def approveRefill(cls,data):
        query = 'UPDATE medications SET refill_request = 2, refills = refills - 1 WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def declineRefill(cls,data):
        query = 'UPDATE medications SET refill_request = 3 WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def refill_completed(cls,data):
        query = 'update medications set refill_request = 0 where id= %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data, med_id):
        query = f'update medications set name = "name", directions = "directions", days_left = "days_left", refills = "refills" where id = {med_id}'
        return connectToMySQL(db).query_db(query, data)

#    @classmethod
#    def medsToBeRefilled(cls, data):
#        query = "SELECT * FROM medications JOIN patients ON medications.patient_id = patients.id JOIN pharmacies ON medications.pharmacy_id = %(pharmacy_id)s WHERE medications.patient_id = %(id)s;"
#        results = connectToMySQL(db).query_db(query, data)
#        pprint(results[0], sort_dicts=False)
#        refills = cls(results[0])
#        for row in results:
#            patient_data = {
#                'id' : row['patients.id'],
#                'first_name' : row['first_name'],
#                'directions' : row['directions'],
#                'last_name' : row['last_name'],
#                'email' : row['email'],
#                'address' : row['address'],
#                'password' : row['password'],
#                'bdate' : row['bdate'],
#                'created_at' : row['created_at'],
#                'updated_at' : row['updated_at']
#            }
#            pharmacy_data = {
#                'id' : row['pharmacies.id'],
#                'name' : row['pharmacies.name'],
#                'email' : row['pharmacies.email'],
#                'password' : row['pharmacies.password'],
#                'address' : row['pharmacies.address'],
#                'nr' : row['nr'],
#                'created_at' : row['pharmacies.created_at'],
#                'updated_at' : row['pharmacies.updated_at']
#            }
#            print('pharmacy to refill med is ', row['pharmacies.name'])
#            refills.patient = patient.Patient(patient_data)
#            refills.pharmacy = pharmacy.Pharmacy(pharmacy_data)
#        return refills


    @staticmethod
    def validate_inputs(data):
        is_valid = True
        if len(data['name'])<3:
            flash('Please choose a valid medication name', "med")
            is_valid = False
        if len(data['directions'])<5:
            flash('Please enter valid directions', "med")
            is_valid = False
        if (data['days_left']).isnumeric() == False or (int(data['days_left']))<1:
            flash("Please enter a valid number for the days left until you finish this prescription", "med")
            is_valid = False
        if (data['days_left']).isnumeric() == False:
            flash("Please enter a valid number of refills this prescription", "med")
            is_valid = False
        return is_valid

