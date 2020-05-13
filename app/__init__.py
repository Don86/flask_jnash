from flask import Flask

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

# Changing configs based on envs based on if-elifs
# Commenting out
#if app.config["ENV"] == "production":
#    app.config.from_object("config.ProductionConfig")

from app import views
from app import admin_views