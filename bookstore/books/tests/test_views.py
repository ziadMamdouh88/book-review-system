from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from books.models import Book, Review
from datetime import date

User = get_user_model()

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword123'
        )
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )
        self.user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }

    def test_register_user(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')

    def test_user_list_admin_only(self):
        url = reverse('user-list')
        # Unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Regular user
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_endpoint(self):
        url = reverse('user-me')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

class BookViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword123'
        )
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
        self.book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'description': 'New Description',
            'isbn': '9876543210987',
            'publication_date': '2023-02-01',
            'genre': 'Non-Fiction',
            'price': '29.99',
            'content': 'New Content'
        }

    def test_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.data['content'], self.book.content)

    def test_create_book_admin_only(self):
        url = reverse('book-list')
        # Unauthenticated user
        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Regular user
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

class ReviewViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )
        self.user2 = User.objects.create_user(
            email='test2@example.com',
            username='testuser2',
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
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=4,
            comment='Great book!'
        )
        self.review_data = {
            'book': self.book.id,
            'rating': 5,
            'comment': 'Excellent book!'
        }

    def test_create_review(self):
        url = reverse('review-list')
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, self.review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.filter(user=self.user2).count(), 1)

    def test_update_own_review(self):
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.force_authenticate(user=self.user)
        updated_data = {'rating': 3, 'comment': 'Updated comment', 'book': self.book.id}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(self.review.comment, 'Updated comment')

    def test_cannot_update_others_review(self):
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.force_authenticate(user=self.user2)
        updated_data = {'rating': 1, 'comment': 'Bad book', 'book': self.book.id}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)  # Unchanged

    def test_my_reviews_endpoint(self):
        url = reverse('review-my-reviews')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['comment'], 'Great book!')
