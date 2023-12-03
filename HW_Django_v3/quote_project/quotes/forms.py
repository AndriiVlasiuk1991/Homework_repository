from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Tag, Quote, Author

class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']

class AuthorForm(ModelForm):
    fullname = CharField(max_length=50,widget=TextInput())
    born_date = CharField(max_length=50,widget=TextInput())
    born_location = CharField(max_length=50,widget=TextInput())
    description = CharField(widget=TextInput())
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class QuoteForm(ModelForm):
    quote = CharField(min_length=10, max_length=150,
                      required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all(), widget=TextInput())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=CheckboxSelectMultiple())

    class Meta:
        model = Quote
        fields = ['quote', 'author','tags']
