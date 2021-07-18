
import boto3
from botocore.exceptions import ClientError

import click
from flask import current_app, g
from flask.cli import with_appcontext

aws_access_key_id='ASIAZ27L7JUKTCNA4JHO'
aws_secret_access_key='hmdm2p1LxarHt3ZTDfeHIlWXWCMybK/dN+Spz9aO'

def get_db():
    if 'db' not in g:
        g.db = boto3.resource('dynamodb', 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url="dynamodb.us-east-1.amazonaws.com", 
        region_name="us-east-1")
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        #db.close()
        pass

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

    db = get_db()

    try:
        # delete it if it does exist, so we can refresh
        # this will throw an error if the table doesn't exist,
        # so we wrap in try, and finally... 
        table = db.Table("Movies")
        table.delete()

    finally:

        click.echo('Creating table...')

        # Catch that error and create table.
        table = db.create_table(
            TableName='Movies',
            KeySchema=[
                {
                    'AttributeName': 'year',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
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

    click.echo('Initialized the database.')
    return table

def put_movie(title, year, plot, rating):
    
    db = get_db()
    table = db.Table("Movies")

    response = table.put_item(
        TableName='Movies',
        Item={
            'year': year,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )
    return response

def get_movie(title, year):
    
    db = get_db()
    table = db.Table("Movies")

    try:
        response = table.get_item(Key={'year': year, 'title': title})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']