from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book, Review
from datetime import date

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_email_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='testuser2', password='testpassword123')

    def test_username_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='test2@example.com', username='', password='testpassword123')

class BookModelTest(TestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'isbn': '1234567890123',
            'publication_date': date(2023, 1, 1),
            'genre': 'Fiction',
            'price': 19.99,
            'content': 'Test Content'
        }
        self.book = Book.objects.create(**self.book_data)

    def test_book_creation(self):
        self.assertEqual(self.book.title, self.book_data['title'])
        self.assertEqual(self.book.author, self.book_data['author'])
        self.assertEqual(self.book.description, self.book_data['description'])
        self.assertEqual(self.book.isbn, self.book_data['isbn'])
        self.assertEqual(self.book.publication_date, self.book_data['publication_date'])
        self.assertEqual(self.book.genre, self.book_data['genre'])
        self.assertEqual(self.book.price, self.book_data['price'])
        self.assertEqual(self.book.content, self.book_data['content'])

class ReviewModelTest(TestCase):
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
            'book': self.book,
            'user': self.user,
            'rating': 4,
            'comment': 'Great book!'
        }
        self.review = Review.objects.create(**self.review_data)

    def test_review_creation(self):
        self.assertEqual(self.review.book, self.review_data['book'])
        self.assertEqual(self.review.user, self.review_data['user'])
        self.assertEqual(self.review.rating, self.review_data['rating'])
        self.assertEqual(self.review.comment, self.review_data['comment'])

    def test_unique_constraint(self):
        # Test that a user can't review the same book twice
        with self.assertRaises(Exception):
            Review.objects.create(
                book=self.book,
                user=self.user,
                rating=5,
                comment='Another review'
            )
