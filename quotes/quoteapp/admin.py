from django.contrib import admin

from .models import Author, Tag, Quote

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('fullname',)}

admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Quote)