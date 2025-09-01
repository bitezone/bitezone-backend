

## Connecting to AWS RDS

Ensure there is .env file in the directory where you will need the following information
POSTGRES_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_PASSWORD
- ensure the RDS is accepting your IP address if you are connecting locally


## First time setting up django with database

For setting up tables for users in django
```
python3 manage.py migrate 
```

Create a super user for accessing to "/admin" for control
```
python3 manage.py createsuperuser
```


## Starting the Django
```
python3 manage.py runserver
```


## Moving from local to ec2 instance
```
docker build -t bitezone-backend .
docker save -o <location of tar> bitezone-backend

# scp the tar file to the remote host
docker load -i bitezone-backend.tar # on the remote host

docker run --env-file <env_file> -d -p 8000:8000 <image_name>
```