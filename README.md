# Music

## Running locally
First run docker-compose script to get dynamodb running locally:
    docker-compose -f dynamodb/docker-compose.yaml up -d

Set up environment variables:
    $Env:FLASK_ENV = "DEV"
    $Env:FLASK_APP = "music"

Then initialise the db:
    flask init_db

Then run the flask app:
    flask run

## Deploying to EC2
¯\\\_(ツ)\_/¯

### package app
py setup.py bdist_wheel

### ssh cmd
ssh -i [your_key_file_location]/[yourkeyfilename].pem ubuntu@ec2-3-226-251-9.compute-1.amazonaws.com

### stfp
Need to stfp the following via filezilla:
music.whl

### setup
pip install python3-venv
python3 -m venv venv
source env/bin/activate

### install
pip install music-1.0.0-py3-none-any.whl
export FLASK_APP=[music]

Note that music is install by default in venv/lib/python3.8/site-packages/music

### init
flask init_db

### run 
flask run


## Tutorials
Docker for local dynamodb container:
https://betterprogramming.pub/how-to-set-up-a-local-dynamodb-in-a-docker-container-and-perform-the-basic-putitem-getitem-38958237b968

Flask layout:
https://flask.palletsprojects.com/en/2.0.x/tutorial/

Dynamodb crud ops:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html