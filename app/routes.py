from flask import render_template, request, jsonify, redirect, Blueprint
auth_bp = Blueprint("auth", __name__)
from app import db
from app.models import User, Todo
from sqlalchemy import select

# 🎨 1. Front-Facing User Interface Template Mappings
@auth_bp.route("/")
@auth_bp.route("/login")
def render_login_page():
    """Serves the secure profile authentication entrance gate portal page."""
    return render_template("login.html")

@auth_bp.route("/register")
def render_registration_page():
    """Serves the secure user profile registration front-facing portal page."""
    return render_template("register.html")

@auth_bp.route("/dashboard")
def render_dashboard():
    """Serves the dark-theme central task management execution panel dashboard."""
    return render_template("dashboard.html")

# 🔒 2. Backend Security & Session API Processes
@auth_bp.route("/api/login", methods=["POST"])
def api_login_processor():
    data = request.get_json() or {}
    email = data.get("email")
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Target node coordinate not found inside database rows"}), 401
    return jsonify({
        "message": "Authentication gate cleared successfully",
        "user": {"id": int(user.id), "email": str(user.email)}
    }), 200

@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Missing email or password parameters"}), 400
    stmt = select(User).where(User.email == email)
    existing_user = db.session.execute(stmt).scalar()
    if existing_user:
        return jsonify({"error": "Registration conflict: User profile coordinate already active"}), 400
    
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# 🚀 3. Task Management Matrix Processing Engines
@auth_bp.route("/api/todos", methods=["POST"])
def create_task():
    try:
        data = request.get_json() or {}
        new_todo = Todo(
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority", "Medium"),
            category=data.get("category", "Operations"),
            user_id=data.get("user_id")
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({
            "message": "Task row deployed successfully into PostgreSQL cache rails",
            "task": {"id": new_todo.id, "title": new_todo.title}
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Task deployment failure: {str(e)}"}), 500

@auth_bp.route("/api/todos", methods=["GET"])
def get_tasks():
    user_id = request.args.get("user_id", 1)
    try:
        stmt = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        tasks = db.session.execute(stmt).scalars().all()
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
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_task(todo_id):
    try:
        todo = db.session.get(Todo, todo_id)
        if not todo:
            return jsonify({"error": "Task target not found in PostgreSQL cache"}), 404
        
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Task row purged successfully from relational rails"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Task purge failure: {str(e)}"}), 500

