from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        '''Setting up before each test'''
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        '''Testing that the root path renders all that it should'''
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        '''testing the ability to find a valid word in the board and our dictionary'''
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "E", "L", "L", "O"], 
                                 ["B", "O", "O", "T", "Y"], 
                                 ["C", "H", "A", "R", "T"], 
                                 ["C", "R", "E", "A", "M"], 
                                 ["A", "P", "P", "L", "E"]]
        response = self.client.get('/check-word?word=hello')
        self.assertEqual(response.json['result'], 'ok')

     def test_invalid_word(self):
        '''testing if it will catch a word not contained on the board'''
        self.client.get('/')
        res = self.client.get('/check-word?word=impossible')
        self.assertEqual(res.json['result'], 'not-on-board')

    def non_english_word(self):
        '''testing if it will catch a word that is not real'''
        self.client.get('/')
        res = self.client.get('/check-word?word=hbcca')
        self.assertEqual(res.json['result'], 'not-word')

