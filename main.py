from app import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database is created inside the app context
    app.run(debug=True, host="0.0.0.0")
