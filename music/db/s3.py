import os, json, sys
from pathlib import Path

import boto3, botocore

import click
from flask import current_app, g
from flask.cli import with_appcontext

"""
S3 functions
"""
def get_s3():
    """
    get_s3
    
    Gets the database. 
    """

    if 's3' not in g:

        if os.environ['FLASK_ENV'] == "dev":
            g.s3 = boto3.resource('s3', endpoint_url="http://localhost:8042")

        else:
            g.s3 = boto3.resource(
                        's3', 
                        region_name="us-east-1")

    return g.s3

def close_s3(e=None):
    """
    close_s3

    Closes the database.
    """
    s3 = g.pop('s3', None)

    if s3 is not None:
        #s3.close()
        pass

"""
Initialisation functions
"""
def init_app(app):
    """
    init_app

    Registers the db with the flask application
    """
    app.teardown_appcontext(close_s3)
    app.cli.add_command(init_s3)

@click.command('init_s3')
@with_appcontext
def init_s3():
    """
    init_s3

    Initialises the s3 database.
    """
    print('Initialising the s3 database... ')

    base_path = Path(__file__).parent
    filename = (base_path / "a2.json").resolve()

    init_imgs(filename)  

    print('s3 Database initialised.')

def init_imgs(filename):
    """
    init_imgs

    Reads data from json and adds images to the s3 bucket
    """
    with open(filename) as file:
        data = json.load(file)

    for img in data['img_url']:
        put_img(img)

def put_img(img):
    """
    put_imgs

    Uploads the passed img to the s3 bucket
    """
    pass