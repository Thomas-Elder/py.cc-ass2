# Music

## Running locally
### Dynamodb 
First run docker-compose script to get dynamodb running locally:

docker-compose -f dynamodb/docker-compose.yaml up -d

### Then initialise the db:
flask init_db

### Then run the flask app:
flask run

## Deploying to EC2
¯\\\_(ツ)\_/¯

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

Dynamodb ref:
https://dynobase.dev/dynamodb-python-with-boto3/

s3 ref:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrations3.html