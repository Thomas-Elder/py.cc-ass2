
import os
import json

import boto3
from botocore.exceptions import ClientError

import click
from flask import current_app, g
from flask.cli import with_appcontext

aws_access_key_id='ASIAZ27L7JUKTCNA4JHO'
aws_secret_access_key='hmdm2p1LxarHt3ZTDfeHIlWXWCMybK/dN+Spz9aO'

def get_db():
    """
    get_db
    
    Gets the database. 
    """

    if 'db' not in g:

        if os.environ['FLASK_ENV'] == "DEV":
            g.db = boto3.resource('dynamodb', endpoint_url="http://localhost:8042")

        else:
            g.db = boto3.resource('dynamodb', 
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            #endpoint_url="dynamodb.us-east-1.amazonaws.com", 
            region_name="us-east-1")

    return g.db

def close_db(e=None):
    """
    close_db

    Closes the database.
    """
    db = g.pop('db', None)

    if db is not None:
        #db.close()
        pass

"""
Initialisation functions.
"""
def init_app(app):
    """
    init_app

    Registers the db with the flask application
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)

@click.command('init_db')
@with_appcontext
def init_db():
    """
    init_db

    Initialises the database. 
    """
    click.echo('Initialising the database... ')

    init_loginTable()
    init_musicTable()

    init_users()
    init_music()  

    click.echo('Database initialised.')

def init_loginTable():
    """
    init_loginTable

    Initialises the login table.
    """
    db = get_db()
    
    # Get the table
    table = db.Table("login")

    click.echo('Creating log in table...')

    try: 

        # Create table.
        table = db.create_table(
            TableName='login',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    except:
        click.echo('Table exists already')

    click.echo('Initialized the login table.')
    return table

def init_musicTable():
    """
    init_musicTable

    Initialises the music table.
    """

    db = get_db()

    # title, artist, year, web_url, image_url
    # Get the table
    table = db.Table("music")

    click.echo('Creating music table...')

    try:

        # Create table.
        table = db.create_table(
            TableName='music',
            KeySchema=[
                {
                    'AttributeName': 'artist',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'  # Sort key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'artist',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    
    except :
        click.echo('Table exists already')

    click.echo('Initialized the music table.')
    return table

def init_users():
    """
    init_users

    Adds the default users to the Users table.
    """
    emails = ['s33750870@student.rmit.edu.au', 's33750871@student.rmit.edu.au', 's33750872@student.rmit.edu.au', 's33750873@student.rmit.edu.au', 's33750874@student.rmit.edu.au', 's33750875@student.rmit.edu.au', 's33750876@student.rmit.edu.au', 's33750877@student.rmit.edu.au','s33750878@student.rmit.edu.au','s33750879@student.rmit.edu.au']
    user_names = ['Tom Elder0', 'Tom Elder1', 'Tom Elder2', 'Tom Elder3', 'Tom Elder4', 'Tom Elder5', 'Tom Elder6', 'Tom Elder7', 'Tom Elder8', 'Tom Elder9']
    passwords = ['012345', '123456', '234567', '345678', '456789', '567890', '678901', '789012', '890123', '901234']

    # users
    for email, user_name, password in zip(emails, user_names, passwords):
        put_user(email, user_name, password)

def init_music():
    pass

"""
USER CRUD Operations
"""
def put_user(email, user_name, password):
    """
    put_user

    Adds the passed user details to the Login table.
    """
    db = get_db()
    table = db.Table("login")

    try:
        response = table.put_item(
            TableName='login',
            Item=
            {
                'email' : email,
                'info' : 
                {
                    'user_name' : user_name,
                    'password': password
                }
            }
        )

        return response

    except:
        click.echo('Error putting user')

    # return response

def get_user(email):
    """
    get_user

    Gets the user with the specified email.

    Parameters
    ----------
    email: the email of the user to return.

    Returns
    -------
    user
    """
    db = get_db()
    table = db.Table("login")

    try:
        response = table.get_item(Key={'email': email})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

def get_users():
    """
    get_users
    
    Gets all users in the login table
    """
    db = get_db()
    table = db.Table("login")

    try:
        response = table.scan()['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


"""
MUSIC CRUD Operations
"""
def put_song(email, user_name, password):
    """
    put_song

    Adds the passed song details to the music table.
    """
    db = get_db()
    table = db.Table("music")

    try:
        response = table.put_item(
            TableName='music',
            Item=
            {
                'email' : email,
                'info' : 
                {
                    'user_name' : user_name,
                    'password': password
                }
            }
        )

        return response

    except:
        click.echo('Error putting user')

def get_song(title, artist):
    """
    get_song

    Gets the song with the specified title and artist.

    Parameters
    ----------
    title: the title of the song
    artist: the artist of the song

    Returns
    -------
    song
    """

    db = get_db()
    table = db.Table("music")

    try:
        response = table.get_item(Key={'title': title, 'artist': artist})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

def get_songs():
    """
    get_songs
    
    Gets all songs in the music table
    """

    db = get_db()
    table = db.Table("music")

    try:
        response = table.scan()['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']