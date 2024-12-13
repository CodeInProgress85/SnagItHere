from app import db
from app.models import User

def delete_user_by_id(user_id):
    user_to_delete = User.query.get(user_id) 

    if user_to_delete: 
        db.session.delete(user_to_delete) 
        db.session.commit() 
        print("User deleted.") 
    else: 
        print("User not found.")
