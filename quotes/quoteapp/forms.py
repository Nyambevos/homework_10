from django.forms import ModelForm, CharField, TextInput

from .models import Authors

class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    born_date = CharField(min_length=3, max_length=30)
    born_location = CharField(min_length=3, max_length=80)
    description = CharField(min_length=3, required=True)

    class Meta:
        model = Authors
        fields = ['fullname', 'born_date', 'born_location', 'description']
