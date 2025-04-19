from rest_framework import serializers
from .models import User, Book, Review
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('email', 'date_joined')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    book_title = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Review
        fields = ('id', 'book', 'book_title', 'user', 'user_id', 'rating', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class BookSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'isbn', 'cover_image', 
                  'publication_date', 'genre', 'price', 'reviews_count', 'average_rating',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return sum(review.rating for review in reviews) / reviews.count()

class BookDetailSerializer(BookSerializer):
    content = serializers.CharField()
    
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ('content',)

class BookWithReviewsSerializer(BookDetailSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta(BookDetailSerializer.Meta):
        fields = BookDetailSerializer.Meta.fields + ('reviews',)
