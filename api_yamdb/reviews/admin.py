from django.contrib import admin

from .models import Categories, Comment, Genres, Review, Title, User

admin.site.register(User)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
