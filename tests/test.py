import json
from api import db
from main import app
from unittest import TestCase
from api.models.user import UserModel
from api.models.note import NoteModel
from base64 import b64encode
from config import Config


class TestUsers(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.drop_all()
            db.create_all()

    # Создаем и залогиниваем пользователя
    def create_and_auth_user(self):
        user_data = {
            "username": 'admin',
            'password': 'admin',
            "role": 'admin'
        }

        user = UserModel(**user_data)
        user.save()
        self.user = user
        # "login:password" --> b64 --> 'ksjadhsadfh474=+d'
        self.headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

    def test_user_creation(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        res = self.client.post('/users',
                               data=json.dumps(user_data),
                               content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('admin', data.values())

    def test_user_get_by_id(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        user = UserModel(**user_data)
        user.save()
        user_id = user.id
        response = self.client.get(f'/users/{user_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["username"], user_data["username"])

    def test_user_not_found_by_id(self):
        response = self.client.get('/users/70')
        self.assertEqual(response.status_code, 404)

    def test_users_get(self):
        users_data = [
            {
                "username": 'admin',
                'password': 'admin'
            },
            {
                "username": 'ivan',
                'password': '12345'
            },
        ]
        for user_data in users_data:
            user = UserModel(**user_data)
            user.save()

        res = self.client.get('/users')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], users_data[0]["username"])
        self.assertEqual(data[1]["username"], users_data[1]["username"])

    def test_user_not_found(self):
        """
        Получение несуществующего пользователя
        """
        res = self.client.get('/users/2')
        self.assertEqual(res.status_code, 404)

    def test_unique_username(self):
        """
        Проверяет невозможность создания нескольких пользователей с одинаковым username
        """
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        res = self.client.post('/users',
                               data=json.dumps(user_data),
                               content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('admin', data.values())

        res = self.client.post('/users',
                               data=json.dumps(user_data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_edit_user(self):
        """
        Редактирование пользователя
        """
        user_data = {
            "username": 'user',
            'password': 'user'
        }
        user = UserModel(**user_data)
        user.save()
        user_id = user.id

        new_note = {
            "username": 'user1'
        }

        self.create_and_auth_user()

        res = self.client.put(f'/users/{user_id}',
                              headers=self.headers,
                              data=json.dumps(new_note),
                              content_type='application/json')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["username"], new_note["username"])

    def test_delete_user(self):
        """
        Удаление пользователя
        """
        user_data = {
            "username": 'user',
            'password': 'user'
        }
        user = UserModel(**user_data)
        user.save()
        user_id = user.id

        self.create_and_auth_user()
        res = self.client.delete(f'/users/{user_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class TestNotes(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.drop_all()
            db.create_all()

        # Создаем и залогиниваем пользователя
        user_data = {
            "username": 'admin',
            'password': 'admin',
            "role": 'admin'
        }
        self.create_and_auth_user(user_data)

    def create_and_auth_user(self, user_data):
        user = UserModel(**user_data)
        user.save()
        self.user = user
        # "login:password" --> b64 --> 'ksjadhsadfh474=+d'
        self.headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

    def test_create_note(self):
        note_data = {
            "text": 'Test note 1',
            "private": False
        }
        res = self.client.post('/notes',
                               headers=self.headers,
                               data=json.dumps(note_data),
                               content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data["text"], note_data["text"])
        self.assertFalse(data["private"])

    def test_get_notes(self):
        notes_data = [
            {
                "text": 'Test note 1',
            },
            {
                "text": 'Test note 2',
            },
        ]
        for note_data in notes_data:
            note = NoteModel(author_id=self.user.id, **note_data)
            note.save()

        res = self.client.get('/notes', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_get_note_by_id(self):
        notes_data = [
            {
                "text": 'Test note 1',
            },
            {
                "text": 'Test note 2',
            },
            {
                "text": 'Test note 3',
            },
        ]
        for note_data in notes_data:
            note = NoteModel(author_id=self.user.id, **note_data)
            note.save()
        res = self.client.get('/notes/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["text"], notes_data[0]["text"])

    def test_get_note_another_user(self):
        alex_notes_data = [
            {
                "text": 'Alex note 1',
            },
            {
                "text": 'Alex note 2',
            },
        ]
        user_alex_data = {
            "username": 'alex',
            'password': 'alex'
        }
        user_alex = UserModel(**user_alex_data)
        user_alex.save()
        for note_data in alex_notes_data:
            note = NoteModel(author_id=user_alex.id, **note_data)
            note.save()

        res = self.client.get('/notes/1', headers=self.headers)
        self.assertEqual(res.status_code, 403)

    def test_note_not_found(self):
        """
        Получение заметки с несуществующим id
        """
        res = self.client.get('/notes/2', headers=self.headers)
        self.assertEqual(res.status_code, 404)

    def test_private_public_notes(self):
        """
        Проверка создания/получения публичных/приватных заметок
        """
        notes_data = [
            {
                "text": 'Public Test note 1',
                "private": False
            },
            {
                "text": 'Private Test note 2',
            },
            {
                "text": 'Private Test note 3',
                "private": True
            },
        ]
        ids = []
        for note_data in notes_data:
            note = NoteModel(author_id=self.user.id, **note_data)
            note.save()
            ids.append(note.id)

        res = self.client.get('/notes', headers=self.headers)
        data = json.loads(res.data)

        self.assertFalse(data[0]["private"])
        self.assertTrue(data[1]["private"])
        self.assertTrue(data[2]["private"])

    def test_edit_note(self):
        """
        Редактирование заметки
        """
        notes_data = [
            {
                "text": 'Test note 1',
                "private": False,
            },
            {
                "text": 'Test note 2',
                "private": False,
            }
        ]
        ids = []
        for note_data in notes_data:
            note = NoteModel(author_id=self.user.id, **note_data)
            note.save()
            ids.append(note.id)

        new_note = {
            "text": 'Test 1',
            "private": False,
        }

        res = self.client.put('/notes/2',
                              headers=self.headers,
                              data=json.dumps(new_note),
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["text"], new_note["text"])
        self.assertEqual(data["private"], new_note["private"])

    def test_delete_note(self):
        """
        Удаление заметки
        """
        notes_data = [
            {
                "text": 'Test note 1',
            },
            {
                "text": 'Test note 2',
            }
        ]
        ids = []
        for note_data in notes_data:
            note = NoteModel(author_id=self.user.id, **note_data)
            note.save()
            ids.append(note.id)

        res = self.client.delete('/notes/2', headers=self.headers)
        # data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["text"], notes_data[0]["text"])

    def test_delete_not_found_note(self):
        """
        Удаление заметки
        """
        notes_data = [
            {
                "text": 'Test note 1',
            },
            {
                "text": 'Test note 2',
            }
        ]
        ids = []
        for note_data in notes_data:
            note = NoteModel(author_id=self.user.id, **note_data)
            note.save()
            ids.append(note.id)

        res = self.client.delete('/notes/3', headers=self.headers)
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
