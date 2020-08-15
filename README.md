# Full Stack Web Developer Nanodegree Casting Agency API Backend  

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within 
the company and are creating a system to simplify and streamline your process.

The goal of this project is to demonstarte the skills of using Flask, SQLAlchemy, Auth0 and Heroku to develop and delpoy a RESTful API. This
project is a capstone project of Udacity's Full Stack Web Developer Nanodegree Program.

## Getting Started

### Installing Dependencies
The following dependencies can be installed through running this command in your local command line tool.

```pip install -r requirements.txt```

This app requires Python 3.7 to run.

## Your Task
### Building data models in database/models.py:
Models:
Movies with attributes title and release date
Actors with attributes name, age and gender

### Complete the following endpoints setups in backend/app.py
Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

### Configure roles on Auth0
-Casting Assistant

   -`get:actors` `get:movies`
   
-Casting Director

   -`get:actors`, `get:movies`, `post:actors`, `delete:actors`, `patch:actors`, `patch:movies`
   
-Executive Producer

   -can perform all actions

### Create new API permissions for the created roles:
-get:actors, get:movies
-post:actors, post:movies
-patch:actors, patch:movies
-delete:actors, delete:movies

# Testing
## Testing endpoints with Postman.
   Register three users on Auth0 and assign different roles to each user.
   Sign into each user's account and get them JWT tokens.
   Import postman collection json files. (it's written specifially for this app)
   Run testing with the imported postman jsons collections with designated JWT.
   Export the result of collection and then upload them to the github for review.

# Authors
Po Tin Mak and The Udacity are the authos of this project.

# URL for the App
 https://protected-sands-50014.herokuapp.com



