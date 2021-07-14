# Music

## Running
First run docker-compose script to get dynamodb running locally:
    docker-compose -f dynamodb/docker-compose.yaml up -d

Then initialise the db:
    flask init_db

Then run the flask app:
    flask run