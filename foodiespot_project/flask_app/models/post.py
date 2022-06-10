from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Post:
    db_name = 'foodiespot_schema'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.user_id = db_data['user_id']
        self.community_id = db_data['community_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def posts_to_user(cls):
        query = "SELECT * FROM posts JOIN users ON users.id = user_id ORDER BY posts.created_at asc;"
        results =  connectToMySQL("foodiespot_schema").query_db(query)
        all_post = []
        if results:
            for row in results:
                one_post = cls(row)
                user_data ={
                    **row,
                    "id" : row['users.id'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at'],
                }
                one_post.holder = user.User(user_data)
                all_post.append(one_post)
            return all_post

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (content,user_id,community_id,created_at,updated_at) VALUES (%(content)s,%(user_id)s,%(community_id)s,NOW(),NOW());"
        return connectToMySQL(cls.db_name).query_db(query,data)