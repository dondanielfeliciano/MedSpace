from datetime import datetime
from re import X
from flask_app.config.mysqlconnection import connectToMySQL
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
        # self.bought_cars = []

    @classmethod
    def save(cls,data):
        query = 'insert into medications (name, directions, days_left, refills, patient_id, pharmacy_id) values (%(name)s, %(directions)s, %(days_left)s, %(refills)s, %(patient_id)s, %(pharmacy_id)s)'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_one_med(cls, data):
        query = 'select * from medications where id = %(id)s'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_meds_one_patient_one_pharmacy(cls, data):
        query = 'select * from medications where patient_id = %(patient_id)s and pharmacy_id = %(pharmacy_id)s'
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
    def validate_inputs(data):
        is_valid = True
        if len(data['name'])<3:
            flash('Please choose a valid medication name', "med")
            is_valid = False
        if len(data['directions'])<5:
            flash('Please enter valid directions', "med")
            is_valid = False
        if type(data['days_left']) != int:
            flash("Please enter the days left until you finish this prescription as a number", "med")
        if type(data['days_left']) == int and (int(data['days_left']))<1:
            flash('Please enter a valid number for the days left until you finish this prescription', "med")
            is_valid = False
        if type(data['days_left']) != int:
            flash("Please enter the refills left for this prescription as a number", "med")
        if type(data['refills']) == int and (int(data['refills']))<0:
            flash('Please enter a valid number for the days left until you finish this prescription', "med")
            is_valid = False
        return is_valid

