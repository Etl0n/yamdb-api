from django.contrib import admin

from .models import Title, Comment, Review, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    filter_horizontal = ('genre',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'text',
        'score',
        'pub_date',
    )
    search_fields = ('author', 'title', 'text')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'review',
        'text',
        'pub_date',
    )
    search_fields = ('author', 'text', 'pub_date')
    list_filter = ('author',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
