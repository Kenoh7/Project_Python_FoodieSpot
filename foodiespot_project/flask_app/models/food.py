from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Food:
    db = "foodiespot_schema"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.ingredient = data['ingredient']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def foods_to_user(cls):
        query = "SELECT * FROM foods JOIN users ON users.id = user_id;"
        results =  connectToMySQL(cls.db).query_db(query)
        if results:
            for row in results:
                all_foods = []
                one_food = cls(row)
                user_data ={
                    **row,
                    "id" : row['users.id'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at'],
                }
                one_food.holder = user.User(user_data)
                all_foods.append(one_food)
            return all_foods
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO foods(user_id,ingredient,created_at,updated_at) VALUES (%(user_id)s,%(ingredient)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
