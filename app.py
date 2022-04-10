import os
from flask import Flask
from flask_restful import Api
from resources.users import UserRegister, UserDelete
from resources.titles import Browse, AddToList, DeleteFromList, ViewList
from resources.sessions import Login, Logout

app = Flask(__name__)

#app.config['DEBUG'] = True   # required for local testing to create db, commented for cloud hosting

# App configuration: Database and app secret key
db_url = os.environ.get('DATABASE_URL')                                   # For Heroku, comment for local execution 
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("://", "ql://", 1) # For Heroku, comment for local execution
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'             # For Local, comment for Heroku execution  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'QMUL_CC_T12'
api = Api(app)

# Specify End-Points
# Endpoint: Home
@app.route('/')
def home_endpoint():
    text = 'Welcome to World TV Database. \nBrowse your favrourite TV shows and movies. \nSign up and save your watchlist.\
     \nMore features coming up. \nUse service endpoints to use our services'
    return text, 200
# Main services endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(Browse, '/browse/<title>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(AddToList, '/add-to-list')
api.add_resource(DeleteFromList, '/delete-from-list')
api.add_resource(UserDelete, '/delete-user')
api.add_resource(ViewList, '/view-list')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            from models.admin import AdminModel
            db.create_all()
            AdminModel().save_to_db()

    app.run()

