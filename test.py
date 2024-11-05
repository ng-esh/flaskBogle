from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):
    def setUp(self):
        """Set up test client and variables."""
        self.app = app.test_client()
        app.config['TESTING']= True
        self.boggle_game = Boggle()
      

    def test_homepage(self):
        """Test the homepage loads correctly and returns a board."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table class="board">', response.data)

    def test_check_word_valid(self):
        """Test that a valid word returns correct response."""
        with self.app as client:
            with client.session_transaction() as session:
                session['board'] = [['A', 'B', 'C'], 
                                    ['D', 'E', 'F'], 
                                    ['G', 'H', 'I']]
                # Add valid word logic or mock the dictionary check if needed
                session['dictionary'] = ['ABE', 'ABE', 'DINE']  # Example mock dictionary

            response = client.post('/check-word', json={'word': 'ABE'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

    def test_check_word_invalid(self):
        """Test that an invalid word returns the correct response."""
        with self.app as client:
            with client.session_transaction() as session:
                session['board'] = [['A', 'B', 'C'], 
                                    ['D', 'E', 'F'], 
                                    ['G', 'H', 'I']]
                # Ensure that the dictionary doesn't contain 'INVALID'
                session['dictionary'] = ['ABE', 'DINE']  # Mock dictionary without 'INVALID'

            response = client.post('/check-word', json={'word': 'INVALID'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_post_score(self):
        """Test that posting a score updates the session variables correctly."""
        with self.app as client:
            with client.session_transaction() as session:
                session['highscore'] = 5
                session['nplays'] = 2
            
            response = client.post('/post-score', json={"score": 10})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['brokeRecord'], True)

            with client.session_transaction() as session:
                self.assertEqual(session['highscore'], 10)
                self.assertEqual(session['nplays'], 3)

    def test_post_score_no_highscore(self):
        """Test posting a score with no previous highscore."""
        with self.app as client:
            with client.session_transaction() as session:
                session['highscore'] = 0
                session['nplays'] = 0

            response = client.post('/post-score', json={"score": 5})
            self.assertEqual(response.status_code, 200)

            with client.session_transaction() as session:
                self.assertEqual(session['highscore'], 5)
                self.assertEqual(session['nplays'], 1)
