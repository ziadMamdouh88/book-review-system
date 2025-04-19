from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book, Review
from books.serializers import UserSerializer, BookSerializer, ReviewSerializer
from datetime import date
from rest_framework.exceptions import ValidationError

User = get_user_model()

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_valid_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_password_mismatch(self):
        self.user_data['password2'] = 'DifferentPassword123!'
        serializer = UserSerializer(data=self.user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class BookSerializerTest(TestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'isbn': '1234567890123',
            'publication_date': '2023-01-01',
            'genre': 'Fiction',
            'price': '19.99',
            'content': 'Test Content'
        }

    def test_valid_book_serializer(self):
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())

class ReviewSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            isbn='1234567890123',
            publication_date=date(2023, 1, 1),
            genre='Fiction',
            price=19.99,
            content='Test Content'
        )
        self.review_data = {
            'book': self.book.id,
            'rating': 4,
            'comment': 'Great book!'
        }

    def test_valid_review_serializer(self):
        serializer = ReviewSerializer(data=self.review_data)
        self.assertTrue(serializer.is_valid())
