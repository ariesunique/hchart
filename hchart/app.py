from flask import Flask, render_template
from hchart import chart
from hchart.forms import InputForm


def create_app(config_object="hchart.settings"):
    app = Flask(__name__.split(".")[0])    
    app.config.from_object(config_object)
    app.register_blueprint(chart.routes.blueprint)
    register_errorhandlers(app)
    return app


def register_errorhandlers(app):
    """Register error handlers."""
    
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500        
        error_code = getattr(error, "code", 500)
        error_msg = getattr(error, "description", "An error occurred")
        return render_template("index.html", error=True, error_code=error_code, error_msg=error_msg), error_code

    for errcode in [401, 404, 413, 500]:
        app.errorhandler(errcode)(render_error)
    return None