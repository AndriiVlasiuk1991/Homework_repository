from django.forms import ModelForm, CharField, TextInput, ModelChoiceField

from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    born_date = CharField(min_length=10, max_length=50, required=True, widget=TextInput())
    born_loc = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    biography = CharField(min_length=10, max_length=1000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_loc', 'biography']
        # exclude = ['tags']


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, max_length=1000, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all(), widget=TextInput())
    tag = CharField(min_length=5, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tag']
        exclude = ['tags']
