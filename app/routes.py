from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import bcrypt
from sqlalchemy import select # 👈 Add this modern select token here

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    """
    Captures incoming user registrations, hashes passwords using bcrypt, 
    and provisions clean user rows into the PostgreSQL database.
    """
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password parameters"}), 400

    # 🔒 Modern Security Barrier: Query the database matching the exact user record
    stmt = select(User).where(User.email == email)
    existing_user = db.session.execute(stmt).scalar()
    
    if existing_user:
        return jsonify({"error": "An account with this email address already exists"}), 400

    # 🛡️ Process raw text through the bcrypt hashing machine
    salt = bcrypt.gensalt(rounds=12)
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    try:
        new_user = User(email=email, hashed_password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully into Jarboe Digital vault",
            "user_id": new_user.id,
            "email": new_user.email
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database provisioning failure: {str(e)}"}), 500


@auth_bp.route("/api/login", methods=["POST"])
def login_user():
    """
    Captures authentication credentials, validates emails, checks encrypted 
    bcrypt password hashes, and returns clean session validation tokens.
    """
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password parameters"}), 400

    try:
        # 🔍 Search the database matching the exact user record email
        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).scalar()

        # 🔐 Security Check: If user exists, pass plain text password through bcrypt verification
        if user and bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
            return jsonify({
                "status": "success",
                "message": "Authentication authenticated smoothly into matrix node",
                "user": {
                    "id": user.id,
                    "email": user.email
                }
            }), 200
            
        # 🛡️ General security defense fallback message to mask database existence
        return jsonify({"error": "Invalid email coordinate or security password"}), 401

    except Exception as e:
        return jsonify({"error": f"Authentication validation failure: {str(e)}"}), 500



from flask import render_template # Ensure render_template is included at the top imports!
from app.models import Todo
from sqlalchemy import select

# --- USER INTERFACE GATEWAY ROUTE ---


# --- VISUAL INTERFACE BRAND PORTAL ROUTING OUTLETS ---

@auth_bp.route("/register")
def render_registration_page():
    """Serves the secure user profile registration front-facing portal page."""
    return render_template("register.html")

@auth_bp.route("/login")
def render_login_page():
    """Serves the secure profile authentication entrance gate portal page."""
    return render_template("login.html")

@auth_bp.route("/")
def auto_route_root():
    """Intercepts unmapped domain attempts and smoothly directs them straight to registration."""
    return render_template("register.html")



@auth_bp.route("/dashboard")
def render_dashboard():
    """Rerves the dark-theme central task management execution panel dashboard."""
    return render_template("dashboard.html")


# --- OPERATIONAL CRUD DATA ENDPOINTS ---

@auth_bp.route("/api/todos", methods=["POST"])
def create_task():
    """
    Captures manual or raw text task streams, maps them to a database user context,
    and commits a structured item row inside the active PostgreSQL cluster.
    """
    data = request.get_json() or {}
    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority", "Medium")
    category = data.get("category", "General")
    user_id = data.get("user_id", 1) # Fallback to default verified mockup owner profile account

    if not title:
        return jsonify({"error": "Missing title token"}), 400

    try:
        # Construct and scale a pristine relational database record
        new_todo = Todo(
            title=title,
            description=description,
            priority=priority,
            category=category,
            user_id=user_id
        )
        db.session.add(new_todo)
        db.session.commit()

        return jsonify({
            "message": "Task row deployed successfully into PostgreSQL cache rails",
            "task": {
                "id": new_todo.id,
                "title": new_todo.title,
                "priority": new_todo.priority,
                "category": new_todo.category,
                "is_completed": new_todo.is_completed
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Task deployment failure: {str(e)}"}), 500


@auth_bp.route("/api/todos", methods=["GET"])
def get_tasks():
    """Fetches all active contextual task rows allocated to the user out of postgres memory."""
    user_id = request.args.get("user_id", 1)
    
    try:
        # Construct the query statement matching the user context
        stmt = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        
        # 🚀 Pull out the explicit SCALARS matrix array block before loop iteration
        tasks = db.session.execute(stmt).scalars().all()
        
        # Build the structured JSON payload data list cleanly
        task_list = [{
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "category": t.category,
            "is_completed": t.is_completed
        } for t in tasks]
        
        return jsonify(task_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Task aggregation failure: {str(e)}"}), 500


@auth_bp.route("/api/todos/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Intercepts task updates and adjusts priorities, titles, or completion states inside postgres."""
    data = request.get_json() or {}
    todo = db.session.get(Todo, task_id)
    if not todo:
        return jsonify({"error": "Task record not found"}), 404
        
    todo.priority = data.get("priority", todo.priority)
    todo.is_completed = data.get("is_completed", todo.is_completed)
    db.session.commit()
    return jsonify({"message": "Task matrix updated smoothly"}), 200
