import os, json, sys
from pathlib import Path
import requests

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
    bucket_name = "assignment2images"
    create_bucket(bucket_name)

    # DL/Upload images
    base_path = Path(__file__).parent
    filename = (base_path / "a2.json").resolve()

    # Set up tmp_img dir
    os.mkdir(os.path.join(Path(__file__).parent, 'tmp_img')) 

    init_imgs(filename, bucket_name)  

    print('s3 Database initialised.')

def create_bucket(bucket_name):
    """
    create_bucket

    Creates an s3 bucket
    """

    s3 = get_s3()

    if s3.Bucket(bucket_name) in s3.buckets.all():
        print(f'{bucket_name} already exists.')
        return s3.Bucket(bucket_name)

    else: 

        try:
            print(f'Creating new bucket:{bucket_name}')
            bucket = s3.create_bucket(Bucket=bucket_name)

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
        response = requests.get(song['img_url'])

        if response.status_code == 200:

            filename = os.path.split(song['img_url'])[1]
            print(filename)
            with open(os.path.join('tmp_img/', filename), 'wb') as file:
                file.write(response.content)

            put_img('tmp_img/', filename, bucket_name)

        else:
            print(f'Error downloading image error: {response.status_code}')

"""
IMG CRUD Operations
"""
def put_img(path, filename, bucket_name):
    """
    put_imgs

    Uploads the passed img to the s3 bucket
    """
    s3 = get_s3()
    print(path)
    print(filename)
    s3.Object(bucket_name, filename).put(Body=open(os.path.join(path, filename), 'rb'))

def get_img(artist=None):
    """
    get_img

    Returns the public url of the image matching the passed artist-string. 
    If no artist is passed then returns all img urls
    """
    s3 = get_s3()

    bucket_name = 'assignment2images'
    my_bucket = s3.Bucket(bucket_name)

    if artist is not None:
        artist_key = artist + '.jpg'
        params = {'Bucket': bucket_name, 'Key': artist_key}
        url = s3.meta.client.generate_presigned_url('get_object', params)
        final_url = url.split('?')[0].replace("%20", "")
        return final_url

    
    else: 

        urls = []
        
        for file in my_bucket.objects.all():
            params = {'Bucket': bucket_name, 'Key': file.key}
            url = s3.meta.client.generate_presigned_url('get_object', params)
            urls.append(url.split('?')[0])

        return urls
    
