from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import (
    PasswordField,
    TokenObtainPairSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(required=True)
    author = serializers.StringRelatedField()

    def validate_score(self, value):
        if settings.MIN_SCORE <= int(value) <= settings.MAX_SCORE:
            return int(value)
        raise serializers.ValidationError(
            'Оценка должна быть в диапозоне от 1 до 10'
        )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = (
            'name',
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = (
            'name',
            'slug',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
    )
    category = CategorySerializer()
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        read_only = True
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        queryset_avg = Title.objects.annotate(rating=Avg('reviews__score'))
        title = queryset_avg.get(pk=obj.pk)
        if title.rating is None:
            return None
        return round(title.rating)


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def to_representation(self, value):
        return TitleReadSerializer(value).data


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def send_code(self, validated_data):
        code = User.objects.make_random_password()
        send_mail(
            subject="Confirmation code",
            message=code,
            from_email="django@example.com",
            recipient_list=[validated_data.get('email')],
            fail_silently=True,
        )
        validated_data['password'] = make_password(code)
        return validated_data

    def create(self, validated_data):
        validated_data = self.send_code(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self.send_code(validated_data)
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_role(self, value):
        if self.context['view'].me:
            return self.context['request'].user.role
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Делаем так, чтобы пароль добывался из параметра confirmation_code,
    а не password, а также ломаем коды ответов API здорового человека,
    чтобы получилось API заказчика."""

    confirmation_code = PasswordField()

    # Это нужно только для того, чтобы удалить
    # self.fields['password'], иначе ничего не работает.
    # Спасибо авторам simplejwt за шикарный код.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, attrs):
        if not User.objects.filter(username=attrs['username']).exists():
            raise exceptions.NotFound({'username': ['User not found.']})
        attrs['password'] = attrs.pop('confirmation_code', '')
        try:
            data = super().validate(attrs)
        except BaseException as e:
            raise exceptions.ValidationError(
                {'confirmation_code': ['Invalid confirmation code.']}
            ) from e
        return {'token': data['access']}
