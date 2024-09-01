# E-commerce API

This project represents an API for the E-commerce API Assessment.


## Technologies

1. Python 3.11.
2. FastAPI and all its dependencies to the API itself.
3. MongoDB database.
4. motor for async MongoDB operations.


## Settings to E-commerce API

You have to set up a **.env** file based on **.env.sample**. It has 4 attributes to be defined: **MONGO_DB_USER**, **MONGO_DB_PASSWORD**, **MONGO_DB_CLUSTER_URL** and **MONGO_DB_APP_NAME**. **MONGO_DB_USER** is the user created to access the database inside a MongoDB cluster. **MONGO_DB_PASSWORD** is the password created to access the database inside a MongoDB cluster. **MONGO_DB_CLUSTER_URL** is the the url generated when creating a new MongoDB cluster. **MONGO_DB_APP_NAME** is the chosen name in the creating of a MongoDB cluster. 


## Instructions to run application

After cloning the repository, you can run this API using Docker-compose. To set it up, you just need to run the following command:

```docker-compose up --build```

It will create Docker containers based on what is defined inside docker-compose.yml and Dockerfile.
The application runs on port 8000 by default.
