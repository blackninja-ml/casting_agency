import os
import json
import pytest
import unittest

import src.app as app
from flask_sqlalchemy import SQLAlchemy
from src.database.models import setup_db, Movie, Actor, create_and_drop_all
from src import create_app


SECRET = "12345678"
TOKEN_ASSISTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9NXzhhM3dVcHozd1dVRXhsak5KdyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3A4ODgudXMuYXV0aDAuY29tLyIsInN1YiI6Ijl5cllDaFlXdUJwcGZkeU54Rzc2cndZVTFlTk1raWd4QGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk3NDExMzEzLCJleHAiOjE1OTc0OTc3MTMsImF6cCI6Ijl5cllDaFlXdUJwcGZkeU54Rzc2cndZVTFlTk1raWd4IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.SLdj1zxjUVRoxU3VYMfiSL0M7SQdqtfmN3YSc1vlb8HLl6PEbbg8FH3NUSe6saCHSrgiCytlrPrUCOY1QC8eFzzVaqSVpv0dJoSHsthihCGriGfxrBco041GKaGqBtneFYYCvSbGZFgMLaYbiFmE-HBEnbD1izKXuZB0fp4Q1AllUYne9RhkTA84TdRmJJHt5oerlrtKI1lr2yoTwNcSJJb9EGlSPUyA6TQfiCx1q5PlKtqpQoueIZc8WZo4s7SL-sCI2k9-kiHfHx4hvz3O0tF5mejrK6uYUk8cGvB3eGx8pK_Xo9OhrMGRRHBc_-WtU_lB6mwTsGSgQ60tIl7hsQ"
TOKEN_DIRECTOR = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9NXzhhM3dVcHozd1dVRXhsak5KdyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3A4ODgudXMuYXV0aDAuY29tLyIsInN1YiI6Ijl5cllDaFlXdUJwcGZkeU54Rzc2cndZVTFlTk1raWd4QGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk3NDExMzEzLCJleHAiOjE1OTc0OTc3MTMsImF6cCI6Ijl5cllDaFlXdUJwcGZkeU54Rzc2cndZVTFlTk1raWd4IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.SLdj1zxjUVRoxU3VYMfiSL0M7SQdqtfmN3YSc1vlb8HLl6PEbbg8FH3NUSe6saCHSrgiCytlrPrUCOY1QC8eFzzVaqSVpv0dJoSHsthihCGriGfxrBco041GKaGqBtneFYYCvSbGZFgMLaYbiFmE-HBEnbD1izKXuZB0fp4Q1AllUYne9RhkTA84TdRmJJHt5oerlrtKI1lr2yoTwNcSJJb9EGlSPUyA6TQfiCx1q5PlKtqpQoueIZc8WZo4s7SL-sCI2k9-kiHfHx4hvz3O0tF5mejrK6uYUk8cGvB3eGx8pK_Xo9OhrMGRRHBc_-WtU_lB6mwTsGSgQ60tIl7hsQ"
TOKEN_PRODUCER ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9NXzhhM3dVcHozd1dVRXhsak5KdyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3A4ODgudXMuYXV0aDAuY29tLyIsInN1YiI6Ijl5cllDaFlXdUJwcGZkeU54Rzc2cndZVTFlTk1raWd4QGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk3NDExMzEzLCJleHAiOjE1OTc0OTc3MTMsImF6cCI6Ijl5cllDaFlXdUJwcGZkeU54Rzc2cndZVTFlTk1raWd4IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.SLdj1zxjUVRoxU3VYMfiSL0M7SQdqtfmN3YSc1vlb8HLl6PEbbg8FH3NUSe6saCHSrgiCytlrPrUCOY1QC8eFzzVaqSVpv0dJoSHsthihCGriGfxrBco041GKaGqBtneFYYCvSbGZFgMLaYbiFmE-HBEnbD1izKXuZB0fp4Q1AllUYne9RhkTA84TdRmJJHt5oerlrtKI1lr2yoTwNcSJJb9EGlSPUyA6TQfiCx1q5PlKtqpQoueIZc8WZo4s7SL-sCI2k9-kiHfHx4hvz3O0tF5mejrK6uYUk8cGvB3eGx8pK_Xo9OhrMGRRHBc_-WtU_lB6mwTsGSgQ60tIl7hsQ"

EMAIL_ASSISTANT = "castingassistant_mf@example.com"
EMAIL_DIRECTOR = "director_mf@example.com"
EMAIL_PRODUCER = "producer_mf@example.com"


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency's test case"""

    def setUp(self):
    """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:Liszt762!','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

    # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_actor_in_test = {"name" = "Testing", "age" = "Testing", "gender" = "Testing"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    

    def test_actors_list_success(self):
        actor = Actor(name="Yara Shahidi", age="20", gender="female")
        actor.insert()
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))
    
    def test_movies_list_success(self):
        movie = Movie(name="The Sun Is Also A Star", release_date="05/16/2019", genre="Romance")
        movie.insert()
        res = res.client.get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actor.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_homepage(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'],'Welcome To America!')

    def test_list_new_actor_success(self):
        res = self.client.post('/actors', json=self.test_list_new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data['actor']['name'], data['name'])
        actor_added = Actor.query.get(data['actor']['id'])
        self.assertTrue(actor_added)

    def test_list_new_actor_with_missing_details_fail(self):
        new_actor = {
            "name": "testing"
            "gender": "testing"
        }
        res = self.client.post('/actors', data=json.dumps(new_actor), headers={'Content-Type':'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_list_new_movie_with_missing_details_fail(self):
        new_movie = {
            "title": "Bittch"
            "genre": "porno"
        }
        res = self.client.post('/movies', data=json.dumps(new_actor), headers={'Content-Type':'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_delete_actor_success(self):
        actor = Actor(name="Prince", age="52", gender="male")
        actor.insert()
        res = self.client.delete('/actors/%s' % actor.id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/200000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

    def test_update_movie_success(self):
        movie = Movie(title="Corona", release="03/20/1998")
        movie.insert()
        movie_updated = {
            "genre":"horror"
        }
        res = self.client().patch('movies/%s' % (movie.id), 
        data=json.dumps(movie_updated),
        headers={'Content-Type': 'application/json'}
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['genre'], movie.genre)


    def test_update_actor_success(self):
        actor = Actor(name="Corona", genre="male/female/others", age="1")
        actor.insert()
        actor_updated = {
            "age":"0"
        }
        res = self.client().patch('actors/%s' % (actor.id), 
        data=json.dumps(actor_updated),
        headers={'Content-Type': 'application/json'}
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor.age)

    def test_update_movie_fail(self):
        movie_updated = { "title": "Foo", "genre":"nana"}
        res = self.client().patch('movies/100000'), data=json.dumps(movie_updated), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])  

    def test_update_actor_fail(self):
        actor_updated = { "name": "Foo", "gender":"nana"}
        res = self.client().patch('actors/100000'), data=json.dumps(actor_updated), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success']) 

    def test_delete_movies_success(self):
        movie = Actor(title="LALALA", release_data="05022023", genre="malodrama")
        movie.insert()
        res = self.client.delete('/movies/%s' % movie.id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)

    def test_delete_movies_fail(self):
        res = self.client().delete('/movies/400000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['error'],404)
        self.assertEqual(data['movie_id'], movie.id)

    def test_get_movie_fail(self):
        res = self.client().get('/movies?=2000')
        data = json.loads(res.data)
        self.assertEqual(res.status, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies_success(self):
        res = self.client().get('/moves')
        data = json.loads(res.data)
        self.assertEqual(res.status, 200)
        self.assertTrue(data["success"])
        movies = Movie.query.all()
        self.asserEqual(len(data["movies"]), len(movies))

    def test_get_actors_success(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status, 200)
        self.assertTrue(data["success"])
        actors = Actor.query.all()
        self.asserEqual(len(data["actors"]), len(actors))




if __name__ == "__main__":
    unittest.main()