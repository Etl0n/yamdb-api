from reviews.models import Review, Title

from .exceptions import TitleNotExist


def serch_title(id):
    if Title.objects.filter(id=id).exists():
        title = Title.objects.get(id=id)
        return title
    raise TitleNotExist('Вы ввели номер поста которого не существует')


def serch_review(id):
    if Review.objects.filter(id=id).exists():
        review = Review.objects.get(id=id)
        return review
    raise TitleNotExist('Вы ввели номер поста которого не существует')
