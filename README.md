# Music

## Running
First run docker-compose script to get dynamodb running locally:
    docker-compose -f dynamodb/docker-compose.yaml up -d

Then initialise the db:
    flask init_db

Then run the flask app:
    flask run

## Deploying
¯\_(ツ)_/¯

## Tutorials
Docker for local dynamodb container:
https://betterprogramming.pub/how-to-set-up-a-local-dynamodb-in-a-docker-container-and-perform-the-basic-putitem-getitem-38958237b968

Flask layout:
https://flask.palletsprojects.com/en/2.0.x/tutorial/

Dynamodb crud ops:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html