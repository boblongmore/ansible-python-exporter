# ansible-python-exporter

## Create token from aap
1. Create a new user with audit capabilities
2. Login as that user
3. Create token
4. assign that token to ```aap_token``` in the .env file.

## to run container
docker run --env-file .env -p 5000:5000 --name ansible-exporter ansible-exporter
