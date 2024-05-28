from django.db.models import Avg
from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .exceptions import ExistRewies
from .filter import FilterTitle
from .permissions import (
    AuthorAdminModerOrReadOnly,
    IsAdminOrReadOnly,
    IsAdminOrSelf,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from .utils import serch_review, serch_title


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодействия с отзывами в БД,
    привязанным к произведениям, через API."""

    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = serch_title(self.kwargs.get('title_id'))
        rewiews = Review.objects.filter(title=title)
        return rewiews

    def perform_create(self, serializer):
        title = serch_title(self.kwargs.get('title_id'))
        if Review.objects.filter(
            author=self.request.user, title=title
        ).exists():
            raise ExistRewies('Вы уже писали отзыв')
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = serch_title(self.kwargs.get('title_id'))
        if Review.objects.filter(
            author=self.request.user,
            title=title,
        ).exists():
            try:
                serializer.save()
            except IntegrityError:
                Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодействия с комментариями,
    привязынными к отзывам в БД, через API."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = serch_review(self.kwargs.get('review_id'))
        comments = Comment.objects.filter(review=review)
        return comments

    def perform_create(self, serializer):
        review = serch_review(self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        instance = None
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as e:
            if 'username' not in str(e):
                raise e
            username = serializer.initial_data.get('username')
            email = serializer.initial_data.get('email')
            user = User.objects.filter(username=username, email=email)
            if not user.exists():
                raise e
            instance = user.first()
            serializer = self.get_serializer(
                instance, data=request.data, partial=False
            )
            serializer.is_valid(raise_exception=True)
        serializer.save()
        if instance is not None:
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSelf,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('username',)
    ordering = ordering_fields
    me = False

    def detect_me(self):
        if self.kwargs.get('username') == 'me':
            self.me = True
            self.kwargs['username'] = self.request.user.username

    def get_queryset(self):
        self.detect_me()
        queryset = User.objects.all()
        username = self.request.query_params.get('search')
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

    def update(self, request, *args, **kwargs):
        self.detect_me()
        if self.request.method.lower() == 'put':
            raise exceptions.MethodNotAllowed(self.request.method)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.detect_me()
        if self.me:
            raise exceptions.MethodNotAllowed(self.request.method)
        return super().destroy(request, *args, **kwargs)


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score')).order_by(
            'name'
        )
