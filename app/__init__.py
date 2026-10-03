import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    """
    Central Core Factory: Instantiates Flask, hooks the database vault, 
    and spins up structural model tables inside the PostgreSQL container.
    """
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "jarboe_digital_secure_matrix_key")

    db.init_app(app)

    # 🚀 STEP 1: IMPORT MODELS HERE (Inside the function, but before the context block)
    from app.models import User, Todo

    # 🚀 STEP 2: NOW RUN THE CONTEXT BLOCK
    with app.app_context():
        # SQLAlchemy now clearly sees 'User' and 'Todo' in memory and can build them!
        db.create_all()
        print("Jarboe Digital Matrix: PostgreSQL Relational Tables Synchronized Successfully.")

    # 🚀 The blueprint import must happen FIRST!
    from app.routes import auth_bp

    #  THE PERFECT REALIGNMENT (Line 35)
    app.register_blueprint(auth_bp)


    return app
