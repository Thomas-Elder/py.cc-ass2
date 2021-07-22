
import os

import boto3
from botocore.exceptions import ClientError

import click
from flask import current_app, g
from flask.cli import with_appcontext

aws_access_key_id='ASIAZ27L7JUKTCNA4JHO'
aws_secret_access_key='hmdm2p1LxarHt3ZTDfeHIlWXWCMybK/dN+Spz9aO'

def get_db():
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
    db = g.pop('db', None)

    if db is not None:
        #db.close()
        pass

"""
Initialisation functions.
"""
def init_app(app):
    """init_app
    Registers the db with the flask application
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)

@click.command('init_db')
@with_appcontext
def init_db():
    """init_db

    Initialises the database. 
    """

    init_loginTable()
    init_musicTable()

    init_users()
    init_music()  

def init_loginTable():
    db = get_db()

    # Get the table
    table = db.Table("Login")

    print(table)

    # If it already exists, we're going to delete it and re-init
    if table is not None:
        table.delete()

    click.echo('Creating log in table...')

    # Create table.
    table = db.create_table(
        TableName='Login',
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

    click.echo('Initialized the login table.')
    return table

def init_musicTable():
    pass

def init_users():
    """
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
CRUD Operations
"""
def put_user(email, user_name, password):
    """
    Adds the passed user details to the Users table.
    """
    db = get_db()
    table = db.Table("Users")

    response = table.put_item(
        TableName='Users',
        Item=
        {
            'email' : email,
            'user_name' : user_name,
            'info' : 
            {
                'password': password
            }
        }
    )
    return response

def get_user(email, user_name):
    """
    Gets the user with the specified email.
    """
    db = get_db()
    table = db.Table("Users")

    try:
        response = table.get_item(Key={'email': email, 'user_name': user_name})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']