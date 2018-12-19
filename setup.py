#!/usr/bin/env python3
import configparser
from setuptools import setup

def parseCSV(input):
    if input == "":
        return []
    return [a.strip() for a in input.split(",")]

config = configparser.ConfigParser()
config.read("config.ini")

with open("./environment", "w") as f:
    f.write("\n".join([
        "#!/usr/bin/env sh",
        "export PYTHONPATH=$PYTHONPATH:./lib"
        "export FLASK_APP={}".format(config["setup"].get("package", "app"))
    ])+"\n")

setup(
    name = config["setup"].get("name"),
    packages=[config["setup"].get("package", "app")] + parseCSV(config["setup"].get("packages", "")),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy'
    ] + parseCSV(config["setup"].get("requires", "")),
)
