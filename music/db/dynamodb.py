
import os, json, sys

from pathlib import Path

import boto3, botocore

import click

from flask import current_app, g
from flask.cli import with_appcontext

from ..models.user import User
from ..models.song import Song

"""
DyanamoDB functions
"""
def get_db():
    """
    get_db
    
    Gets the database. 
    """

    if 'db' not in g:

        if os.environ['FLASK_ENV'] == "dev":
            g.db = boto3.resource('dynamodb', endpoint_url="http://localhost:8042")

        else:
            g.db = boto3.resource(
                        'dynamodb', 
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
    print('Initialising the database... ')

    base_path = Path(__file__).parent
    songfile = (base_path / "a2.json").resolve()

    init_loginTable()
    init_musicTable()

    init_users()
    init_songs(songfile)  

    for user in get_users():
        print(user)

    print('Database initialised.')

def init_loginTable():
    """
    init_loginTable

    Initialises the login table.
    """
    db = get_db()
    
    # Get the table if it exists. 
    table = db.Table("login")

    print('Creating log in table...')

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

    except Exception as error:
        print(f'Table exists already: {error}')

    print('Initialized the login table.')
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

    print('Creating music table...')

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
    
    except Exception as error:
        print(f'Table exists already: {error}')

    print('Initialized the music table.')
    return table

def init_users():
    """
    init_users

    Adds the default users to the Users table.
    """
    emails = ['s33750870@student.rmit.edu.au', 's33750871@student.rmit.edu.au', 's33750872@student.rmit.edu.au', 's33750873@student.rmit.edu.au', 's33750874@student.rmit.edu.au', 's33750875@student.rmit.edu.au', 's33750876@student.rmit.edu.au', 's33750877@student.rmit.edu.au','s33750878@student.rmit.edu.au','s33750879@student.rmit.edu.au']
    usernames = ['Tom Elder0', 'Tom Elder1', 'Tom Elder2', 'Tom Elder3', 'Tom Elder4', 'Tom Elder5', 'Tom Elder6', 'Tom Elder7', 'Tom Elder8', 'Tom Elder9']
    passwords = ['012345', '123456', '234567', '345678', '456789', '567890', '678901', '789012', '890123', '901234']
    usersongs = []

    # users
    for email, username, password in zip(emails, usernames, passwords):
        put_user(email, username, password, usersongs)

def init_songs(songfile):
    """
    init_songs

    Reads songs from json and adds them to music table
    """

    with open(songfile) as file:
        data = json.load(file)

    for song in data['songs']:
        put_song(song['artist'], song['title'], song['year'], song['web_url'], song['img_url'])

"""
USER CRUD Operations
"""
def put_user(email, username, password, usersongs):
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
                'username' : username,
                'password': password,
                'usersongs': usersongs

            }
        )

        return response

    except Exception as error:
        print(f'Error putting user: {error}')

    print(f'User added: {email}:{username}:{password}')

    # return response

def get_user(email=None):
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
    except Exception as error:
        print(f'Error getting user: {error}')
    else:
        if 'Item' in response:

            return User(response['Item']['email'], response['Item']['email'], response['Item']['username'], response['Item']['password'], response['Item']['usersongs'])

        else:
            return None

def get_users():
    """
    get_users
    
    Gets all users in the login table
    """
    db = get_db()
    table = db.Table("login")

    try:
        response = table.scan()['Items']
    except Exception as error:
        print(f'Error getting users: {error}')
    else:
        users = []
        for record in response:
            users.append(User(record['email'], record['email'], record['username'], record['password'], record['usersongs']))

        return users

"""
MUSIC CRUD Operations
"""
def put_song(artist, title, year, web_url, img_url):
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
                'artist' : artist,
                'title' : title,
                'year' : year,
                'web_url' : web_url,
                'img_url' : img_url
            }
        )

        return response

    except Exception as error:
        print(f'Error putting song: {error}')

def get_song(artist=None, title=None):
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
        response = table.get_item(Key={'artist': artist, 'title': title})
    except Exception as error:
        print(f'Error getting song: {error}')
    else:
        if 'Item' in response:
            return response['Item']
        else:
            return None

def get_songs(artist=None, title=None, year=None):
    """
    get_songs
    
    Gets all songs in the music table
    """

    db = get_db()
    table = db.Table("music")

    try:
        response = table.scan()['Items']
    except Exception as error:
        print(f'Error getting songs: {error}')
    else:
        songs = []
        for record in response:
            songs.append(Song(record['artist'], record['artist'], record['year'], record['web_url']))
            
        return songs

"""
SUBSCRIPTION CRUD Operations
"""
def get_user_songs(useremail):
    """
    Returns the list of songs the user has subscribed to.
    """
    user = get_user(useremail)

    songs = []
    for record in user.usersongs:
        song = get_song(artist=record['artist'], title=record['title'])
        songs.append(Song(song['artist'], song['artist'], song['year'], song['web_url']))

    return songs

def put_user_song(useremail, songartist, songtitle):
    """
    Adds the given song to the users usersong table entry.
    """
    user = get_user(useremail)
    user.usersongs.append({'artist': songartist, 'title': songtitle})
    put_user(user.email, user.username, user.password, user.usersongs)

def rm_user_song(useremail, songartist, songtitle):
    """
    Removes the given song to the users usersong table entry.
    """
    user = get_user(useremail)

    temp = list(filter(lambda song: song['title'] != songtitle and song['artist'] != songartist, user.usersongs))

    put_user(user.email, user.username, user.password, temp)
            
