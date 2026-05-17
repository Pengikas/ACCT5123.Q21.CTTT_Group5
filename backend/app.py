# app.py
from flask import Flask
from backend.config import Config

# Import blueprints
from backend.routes.employee_routes import employee_bp
from backend.routes.prediction_routes import prediction_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.analytics_routes import analytics_bp
from backend.routes.report_routes import report_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(report_bp)


@app.route('/')
def home():
    return {
        "message": "Employee Attrition Prediction API",
        "status": "running",
        "version": "1.0"
    }


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)