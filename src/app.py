import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
import sys

from .database.models import db_drop_and_create_all, setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #setup_migrations(app)
  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                             "Content-Tpe,Authorization,true")
    response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
    return response


  @app.route('/')
  def index():
    return jsonify({
      "success": True,
      "message": "Welcome to America!"
    })

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def retrieve_actors(jwt):
    actors = Actor.query.order_by(Actor.id).all()
    
    if (len(actors) == 0):
      abort(404)

    else:
      return jsonify({
        "actors": [actor.format() for actor in actors],
        "success": True,
      })

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def retrieve_movies(jwt):
    movies = Movie.query.order_by(Movie.id).all()

    if (len(movies)==0):
      abort (404)
    
    else:
      return jsonify({
        "movies" : [movie.format() for movie in movies],
        "success" : True,
      })


  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movies(jwt):
    try:
      data = request.get_json()
      if (('title' not in data) or ('release_date' not in data) or ('genre' not in data)):
        abort (404)
      
      movie = Movie(title=data['title'],
                      release_date=datetime.date.fromisoformat(data['release_date']), 
                      genre=data['genre'])
      movie.insert()
      return jsonify({
        "success" : True,
        "movie_id": movie.id
      })
    except:
      abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actors(jwt):
    try:
      data = request.get_json()
      if (('name' not in data) or ('age' not in data) or ('genre' not in data)):
        abort (404)
      
      actor = Actor(name=data['actor'], age=data['age'], genre=data['genre'] )
      actor.insert()
      return jsonify({
        "success":True,
        "actor_id":actor.id,
      })
    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    try:
      movie = Movie.query.filter(Movie.id==movie_id).one_or_none()

      if movie is None:
        abort(404)
      
      movie.delete()
      return jsonify({
        "success":True,
        "movie_id": movie.id,
      })
    
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_movie(jwt, actor_id):
    try:
      actor = Actor.query.filter(Actor.id==actor_id).one_or_none()

      if actor is None:
        abort (404)
      
      actor.delete()
      
      return jsonify({
        "success": True,
        "actor_id": actor.id,
      })
    
    except:
      abort (422)


  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(jwt, actor_id):
    actor = Actor.query(Actor.id==actor_id).one_or_none()

    if actor is None:
      abort(404)

    try:
      data = request.get_json()
      if actor is None:
        abort (404)
      
      if 'name' in data:
        actor.name = data["name"]
      
      if 'age' in data:
        actor.age = data["age"]

      if 'gender' in data:
        actor.gender = data["gender"]

      actor.update()

      return jsonify({
        "success": True,
        "actor": actor.get_formatted_json()
      })
    
    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def patch_movie(jwt, movie_id):
    
    movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
      
    if movie is None:
      abort(404)
    try:

      data = request.get_json()
      if movie is None:
        abort(404)
      
      if 'title' in data:
        movie.title = data["title"]

      if 'release_data' in data:
        movie.release_data = data['release_data']

      if 'genre' in data:
        movie.genre = data['genre']

      movie.update()
      
      return jsonify({
        "success": True,
        "movie": movie.get_formatted_json()
      })

    except:
      abort (422)

  @app.route('/actors')
  @requires_auth('view:actors')
  def view_actors(jwt):
    try: 
      actors = Actor.query.order_by(Actor.id).all()

      if len(actors)==0:
        abort(404)

      actors = [actor.get_formatted_json() for actor in actors]
      return jsonify({
        "success":True,
        "actors": actors
      })
    except:
      abort(422)
      

      
  @app.route('/movies')
  @requires_auth('view:movies')
  def view_movies(jwt):
    try:
      movies = Movie.query.order_by(Movie.id).all()
    
      if len(movies)==0:
        abort(404)

      movies = [movie.get_formatted_json() for movie in movies]
      return jsonify({
        "success": True,
        "movies": movies
    })

    except:
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "message": "Resource not found",
      "error":404,

    }),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "message": "Unprocessable",
      "error":422
    }),422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "succes": False,
      "message": "Server Error",
      "error": 500
    }), 500
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success": False,
      "message": "Not Allowed",
      "error": 405
    }), 405

  @app.errorhandler(401)
  def auth_error(error):
    return jsonify({
      "success": False,
      "message": "Authorization Error",
      "error": 401,
    }), 401

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
      "success": False,
      "message": "Forbidden",
      "error": 403,
    }), 403

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      "success": False,
      "message": error.error,
      "error": error.status_code,
    }), error.status_code

  return app


APP = create_app()
'''
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
'''
