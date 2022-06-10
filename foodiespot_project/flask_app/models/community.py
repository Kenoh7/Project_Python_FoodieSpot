from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Community:
    db = "foodiespot_schema"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def communities_to_user(cls):
        query = "SELECT * FROM communities JOIN users ON users.id = user_id;"
        results =  connectToMySQL(cls.db).query_db(query)
        if results:
            all_community = []
            for row in results:
                one_community = cls(row)
                user_data ={
                    **row,
                    "id" : row['users.id'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at'],
                }
                one_community.holder = user.User(user_data)
                all_community.append(one_community)
            return all_community

    @classmethod
    def onecommunity_to_user(cls,data):
        query = "SELECT * FROM communities JOIN users ON users.id = user_id WHERE communities.id = %(id)s;"
        results =  connectToMySQL(cls.db).query_db(query,data)
        if results:
            row = results[0]
            one_community = cls(row)
            user_data = {
                **row,
                "id" : row['users.id'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
            }
            one_community.holder = user.User(user_data)
            return one_community


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM communities WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def save(cls,data):
        query = "INSERT INTO communities(user_id, title, description,created_at,updated_at) VALUES (%(user_id)s,%(title)s,%(description)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def is_valid(community):
        is_valid = True
        if community['title'] == "":
            is_valid = False
            flash("Please enter a title!!","community")
        if community['description'] == "":
            is_valid = False
            flash("Please fill out the description!!","community")
        return is_valid

    @staticmethod
    def post_is_valid(post):
        is_valid = True
        if post['post'] == "":
            is_valid = False
            flash("Please enter a post!!","post")
        return is_valid
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM communities WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE communities SET title=%(title)s,description=%(description)s,updated_at= NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)