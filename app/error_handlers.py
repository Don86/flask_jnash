from app import app
from flask import render_template, request

@app.errorhandler(404)
def not_found(e):
    """input `e` is the error. 
    """
    print(e)
    return render_template("public/404.html")

@app.errorhandler(500)
def server_found(e):
    print(e)
    # log the error
    app.logger.error(f"Server error: {e}, route: {request.url}")
    return render_template("public/500.html")