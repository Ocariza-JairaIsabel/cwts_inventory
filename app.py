from flask import Flask
from database import init_db
from routes.items import items_bp
from routes.logs import logs_bp

app = Flask(__name__)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(items_bp)
app.register_blueprint(logs_bp)

if __name__ == '__main__':
    app.run(debug=True)
