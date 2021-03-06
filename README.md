# Music
A simple application allowing users to register, log in and query a list of music. They can then subscribe to any song and view a list of a subscribed items. 

## Running locally
### Dynamodb 
First run docker-compose script to get dynamodb running locally:

docker-compose -f dynamodb/docker-compose.yaml up -d

### Then initialise the dbs:
flask init_db

### Initialise s3
flask init_s3
This only needs to be done once. Also this only runs from the ec2 instance, permissions are not set for this to be run from the local instance.

### Then run the flask app:
flask run

## Deploying to EC2
### package app
py setup.py bdist_wheel

### ssh cmd
ssh -i [your_key_file_location]/[your_key_filename].pem ubuntu@[your_ec2_instance_public_dns]

### stfp
Need to stfp the wheel via filezilla
dist\music-1.0.0-py3-none-any.whl

### setup
First update:
apt-get update

#### python and pip
Double check python is there:
python3 --version

Install pip, first dl and install package
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user

.profile has a script that exports LOCAL_PATH to PATH to make pip available for use:
source ~/PROFILE_SCRIPT

Then install and activate venv:
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate

### install
pip install music-1.0.0-py3-none-any.whl
Note that music is install by default in venv/lib/python3.8/site-packages/music

### init
These commands only need running once. 
flask init_s3
flask init_db

### run 
flask run

## Tutorials/References
Docker for local dynamodb container:
https://betterprogramming.pub/how-to-set-up-a-local-dynamodb-in-a-docker-container-and-perform-the-basic-putitem-getitem-38958237b968

Flask layout:
https://flask.palletsprojects.com/en/2.0.x/tutorial/

Dynamodb crud ops:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html

Dynamodb ref:
https://dynobase.dev/dynamodb-python-with-boto3/

s3 ref:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrations3.html