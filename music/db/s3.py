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

    # Set up bucket
    bucket_name = "music_imgs"
    create_bucket(bucket_name)

    # DL/Upload images
    base_path = Path(__file__).parent
    filename = (base_path / "a2.json").resolve()
    init_imgs(filename, bucket_name)  

    print('s3 Database initialised.')

def create_bucket(bucket_name):
    """
    create_bucket

    Creates an s3 bucket
    """

    s3 = get_s3()

    try:
        print('\nCreating new bucket:', bucket_name)
        bucket = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': "us-east-1"
            }
        )

        bucket.wait_until_exists()
        print(f'Bucket successfully created as {bucket_name} in "us-east-1"')

    except Exception as error:
        print(f'Error creating bucket: {error}')

    else:
        return bucket
    

def init_imgs(filename, bucket_name):
    """
    init_imgs

    Reads data from json and adds images to the s3 bucket
    """
    with open(filename) as file:
        data = json.load(file)

    for song in data['songs']:
        put_img(song['img_url'], bucket_name)

def put_img(img_url, bucket_name):
    """
    put_imgs

    Uploads the passed img to the s3 bucket
    """
    s3 = get_s3()

    s3.meta.client.upload_file(img_url, bucket_name, img_url)