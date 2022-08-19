from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import pharmacy
import re
import datetime
from flask import flash, session
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


db='medspace'


class Patient:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.address = data['address']
        self.bdate = data['bdate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.bought_cars = []

    @classmethod
    def registration(cls,data):
        query = 'insert into patients (first_name, last_name, email, password, address, bdate) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(address)s, %(bdate)s)'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_one_patient(cls, data):
        query = 'select * from patients where id = %(id)s'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_patient_by_email(cls,data):
        query = 'select * from patients where email = %(email)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def add_pharmacy(cls,data):
        query = 'insert into patients_pharmacies (patient_id, pharmacy_id) values (%(patient_id)s, %(pharmacy_id)s)'
        return connectToMySQL(db).query_db(query, data)

    # @classmethod
    # def get_bought_cars(cls,data):
    #     query = 'select * from users as buyers left join cars on buyers.id = cars.buyer_id left join users as sellers on sellers.id = cars.seller_id where buyers.id = %(id)s'
    #     results = connectToMySQL(db).query_db(query, data)
    #     buyer = cls(results[0])
    #     for row in results:
    #         car_data = {
    #             "id" : row['cars.id'],
    #             "make": row['make'],
    #             "model": row['model'],
    #             "year": row['year'],
    #             "price" : row['price'],
    #             "description" : row['description'],
    #             "seller_id" : row['sellers.id'],
    #             "buyer_id" : session['user_id'],
    #             "created_at": row['cars.created_at'],
    #             "updated_at": row['cars.updated_at'],
    #             "first_name" : row['sellers.first_name'],
    #             "last_name" : row['sellers.last_name']
    #         }
    #         buyer.bought_cars.append(car.Car(car_data))
    #     return buyer

    @staticmethod
    def validate_inputs(patient):
        is_valid = True
        if Patient.get_patient_by_email({'email': patient['email']}):
            flash ('This email is already associated with another account.', 'patient_registration')
            is_valid = False
        if not EMAIL_REGEX.match(patient['email']):
            flash('This is an invalid email address.',"patient_registration")
            is_valid = False
        if len(patient['first_name'])<3:
            flash('Please choose a first name that is at least 3 charachters long.', "patient_registration")
            is_valid = False
        if len(patient['last_name'])<3:
            flash('Please choose a last name that is at least 3 charachters long.', "patient_registration")
            is_valid = False
        if len(patient['password'])<8:
            flash('Please choose a password that is at least 8 charachters long.', "patient_registration")
            is_valid = False
        if patient['password'] != patient['confirm_password']:
            flash('Please make sure that your password is typed the same way in both fields.',"patient_registration")
            is_valid = False
        if len(patient['address']) < 10:
            flash('Please chosse a valid address', "patient_registration")
            is_valid = False
        if patient['bdate'][:4] > datetime.datetime.now().strftime("%Y"):
            flash('Please enter a valid date of birth', 'patient_registration')
            is_valid = False
        # continue verfication if the date of birth is in the past
        return is_valid

