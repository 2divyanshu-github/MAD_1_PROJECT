from flask import Flask
from application.database import db #step3
app = None

def create_app():
  app= Flask(__name__)
  app.debug = True
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ebook.sqlite3" #step3
  db.init_app(app) #step3
  app.app_context().push()
  return app

app = create_app()
from application.controllers import * #step 2
# from application.models import *

if __name__ == '__main__':
  # db.create_all()
  # user1 = User(username="admin123",email="admin@user.com",password="1234",type="admin")
  # db.session.add(user1)
  # db.session.commit()
  app.run()