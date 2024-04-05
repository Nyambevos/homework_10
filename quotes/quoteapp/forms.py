from django.forms import ModelForm, CharField, TextInput, SlugField

from .models import Author, Tag, Quote

class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    born_date = CharField(min_length=3, max_length=30)
    born_location = CharField(min_length=3, max_length=80)
    description = CharField(min_length=3, required=True)

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(min_length=3, required=True)

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']
