# OVERVIEW

This project aims to stablish a FHIR server, an api for patient information upload, and an assynchronous service to process the data and send to the FHIR server. The FHIR server used is HAPI FHIR, the API is a flask application, and the assynchronous processing is managed through Redis as a message broker and Celery.

## Prerequisites

You need both docker and docker compose installed to run this application. Python and all the libraries in requirements.txt are also recommended if you intend to use the scripts in /usage to showcase the services.

## Environment Variables

The .env file contains all the environment variables for the FHIR server, the flask application and the celery. It also has the JWT-SECRET-KEY to showcase everything in the project, but in a production environment, this would probably be managed using a secrets manager.

The .env.test contains the variables for a testing environment, which is loaded in config_test.py. The biggest difference here is the usage of different sqlite database file. Also, for a more robust solution in production, it would be advised to use another DB, such as PostgreSQL, which would require other environment variables as well for connection.

## Dockerfile

The dockerfile is the build for both the celery and flask application, since they share the same requirements. As the command to run each is different, it is managed using the docker-compose file.

## Docker-compose

Using the command

```docker compose up```

In the root directory from the repository that all the services are initiated. After initiated, it is important to wait for the FHIR server to be completely started to be able to use the other services as well, since they intend to interact with the FHIR.

The entrypoint for the flask application defines the shell file that will be run once the container is started. This shell file is important to define whether the docker compose is running in a production or development environment. Since the production wasn't implemented, and the gunicorn not installed, that line is commented. But this exemplifies what would be made for a production environment.

## Celery

The flask application calls the celery tasks using their .delay() method. But the celery task has to access the database in order to get the data and register each resource in the FHIR. That would lead to a circular import. The solution used here is that celery iniates another flask application, in which the routes aren't registered, just to manage it's connection with the database, allowing to read the patients which will be written, and deleting them from the database afterwards.

## SNOMED-CT

Given the sample file provided, the conditions and observations found were mapped to their respective SNOMED-CT code for registering in the FHIR server. For a more robust, production environment, it would be better to translate the terms and use the [snomed international API](http://localhost:8080/hapi-fhir-jpaserve) for a more broad registering of observations. The current solution is even implemented using an interface, intended to making the extensability with the API integration easier.

## API Endpoints

### **/login**

**Method**: `POST`

**Description**: Authenticates a user and returns a JWT token that lasts for 1 day.

**Request Payload**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:

- Success: Returns a JSON object containing the access_token.
- Failure: Returns a 401 status code with a message indicating invalid credentials.

**Example**:

```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassword"}'
```

**Example Response**:
```json
{
  "access_token": "your_jwt_token_here"
}
```

### **/upload-csv**

**Method**: POST

**Description**: Uploads a CSV file containing patient data. The data is processed asynchronously and stored in the FHIR server as Patient, Condition, and Observation resources.

**Headers**:

Authorization: Bearer <your_jwt_token_here>


**Request Payload**: A CSV file containing patient data.

**Response**:
- Success: Returns a JSON object containing the file_id that was processed.
- Failure: Returns an error message indicating the issue (e.g., missing file, invalid token).

**Example**:

```bash
curl -X POST http://localhost:5000/upload-csv \
-H "Authorization: Bearer your_jwt_token_here" \
-H "Content-Type: multipart/form-data" \
-F "file=@path_to_your_file.csv"
```

**Example Response**:

```json
{
  "file_id": "unique_file_id"
}
```

## Usage

**create_user.py**

The usage folder is meant to provide an easy way to use the services. The [create_user.py](usage/create_user.py) is a file that creates a test user, provided that one doesn't already exists. Due to the lack of routes to create new user, it is advised that this script is run at least once to create one user, which can in turn generate following JWT.

**get_jwt.py**

The [get_jwt.py](usage/get_jwt.py) is a script that requests a JWT and prints it for usage. This token must afterwards be provided for the /upload-csv route (or the upload_csv.py script) to post data to the API

**upload_csv.py**

The [upload_csv.py](usage/upload_csv.py) is a script to send a CSV file to the API. The JWT should be provided inside the script where it says after being generated, and the path for the CSV file as well.