from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample books'

    def handle(self, *args, **kwargs):
        if Book.objects.exists():
            self.stdout.write(self.style.WARNING('Books already exist in the database. Skipping seeding.'))
            return

        books_data = [
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'description': 'The story of racial injustice and the loss of innocence in the American South during the Great Depression.',
                'isbn': '9780061120084',
                'publication_date': date(1960, 7, 11),
                'genre': 'Fiction',
                'price': 12.99,
                'content': 'Sample content for To Kill a Mockingbird...',
                'cover_image': 'https://example.com/mockingbird.jpg'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'description': 'A dystopian novel set in a totalitarian society ruled by the Party, which has total control over every aspect of people\'s lives.',
                'isbn': '9780451524935',
                'publication_date': date(1949, 6, 8),
                'genre': 'Dystopian',
                'price': 10.99,
                'content': 'Sample content for 1984...',
                'cover_image': 'https://example.com/1984.jpg'
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'description': 'A novel that examines the American Dream and its corruption through the life of Jay Gatsby and his pursuit of wealth and love.',
                'isbn': '9780743273565',
                'publication_date': date(1925, 4, 10),
                'genre': 'Fiction',
                'price': 11.99,
                'content': 'Sample content for The Great Gatsby...',
                'cover_image': 'https://example.com/gatsby.jpg'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'description': 'A romantic novel that follows the character development of Elizabeth Bennet, who learns about the repercussions of hasty judgments.',
                'isbn': '9780141439518',
                'publication_date': date(1813, 1, 28),
                'genre': 'Romance',
                'price': 9.99,
                'content': 'Sample content for Pride and Prejudice...',
                'cover_image': 'https://example.com/pride.jpg'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'description': 'A fantasy novel about the adventures of hobbit Bilbo Baggins, who is hired by the wizard Gandalf to accompany 13 dwarves on a quest to reclaim their treasure.',
                'isbn': '9780547928227',
                'publication_date': date(1937, 9, 21),
                'genre': 'Fantasy',
                'price': 14.99,
                'content': 'Sample content for The Hobbit...',
                'cover_image': 'https://example.com/hobbit.jpg'
            },
        ]

        for book_data in books_data:
            Book.objects.create(**book_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created book: {book_data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(books_data)} books'))
