from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


db='medspace'

class Pharmacy:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.nr = data['nr']
        self.address = data['address']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'insert into pharmacies (name, email, nr, address, password) values (%(name)s, %(email)s,%(nr)s, %(address)s,%(password)s)'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = 'delete from pharmacies where id = %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_pharmacies(cls):
        query = 'select * from pharmacies'
        pharmacies = connectToMySQL(db).query_db(query)
        all_pharmacies = []
        for one_pharmacy in pharmacies:
            all_pharmacies.append(cls(one_pharmacy))
        return all_pharmacies

    @classmethod
    def get_all_unselected_pharmacies(cls,data):
        query = 'select * from pharmacies where id not in (select pharmacy_id from patients_pharmacies where patient_id = %(id)s)'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_pharmacy_by_email(cls,data):
        query = 'select * from pharmacies where email = %(email)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_one_pharmacy(cls, data):
        query = 'select * from pharmacies where id = %(id)s'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def pharmacies_added(cls, data):
        query = 'select * from patients_pharmacies left join pharmacies on pharmacy_id = pharmacies.id where patient_id = %(id)s'
        return connectToMySQL(db).query_db(query, data)


    # @classmethod
    # def get_car_by_id(cls,data):
    #     query = "select * from cars left join users on cars.seller_id = users.id where cars.id = %(id)s"
    #     return connectToMySQL(db).query_db(query,data)

    # @classmethod
    # def update(cls,data, id):
    #     query = f'update cars set price= %(price)s, description= %(description)s, model= %(model)s, make = %(make)s , year = %(year)s where id ={id}'
    #     result = connectToMySQL(db).query_db(query, data)
    #     return result

    # @classmethod
    # def purchase_car(cls,data,id):
    #     query = f'update cars set buyer_id = %(buyer_id)s where id = {id}'
    #     result = connectToMySQL(db).query_db(query,data)
    #     return result

    @staticmethod
    def validate_inputs(data):
        is_valid = True
        if Pharmacy.get_pharmacy_by_email({'email': data['email']}):
            flash ('This email is already associated with another account.', 'pharmacy_registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('This is an invalid email address.',"pharmacy_registration")
            is_valid = False
        if len(data['name']) < 3:
            is_valid = False
            flash('Please display a valid pharmacy name!', 'pharmacy_registration')
        if type(data['nr']) == float:
            is_valid = False
            flash('Please enter a valid store number!', 'pharmacy_registration')
        if len(data['nr']) < 1:
            is_valid = False
            flash('The store number cannot be blank!', 'pharmacy_registration')
        if len(data['address'])<10:
            is_valid = False
            flash('Please enter a valid address!', 'pharmacy_registration')
        if len(data['password'])<8:
            flash('Please choose a password that is at least 8 charachters long.', "pharmacy_registration")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Please make sure that your password is typed the same way in both fields.',"pharmacy_registration")
            is_valid = False
        return is_valid
