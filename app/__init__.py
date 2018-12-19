#!/usr/bin/env python3
from flask import Flask
import os.path
from mako.lookup import TemplateLookup
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

#Module location
if app.debug:
    app.config.from_object('config.Development')
else:
    app.config.from_object('config.Production')

db = SQLAlchemy(app)

lookup = TemplateLookup(
    directories         = [os.path.join(app.config["ROOT_DIR"], "app/views")],
    filesystem_checks   = True,
    module_directory    = os.path.join(app.config["CACHE_DIR"], "modules/"),
    input_encoding      = 'utf-8',
    output_encoding     = "utf-8",
    encoding_errors     = "replace",
    cache_enabled       = False,
    cache_args          = {
        'dir': os.path.join(app.config["CACHE_DIR"], "mako/")
    }
)

def render_template(uri, *args, **kwargs):
    template = lookup.get_template(uri)
    return template.render(*args, **kwargs)

render_template = render_template

from .controllers import *
