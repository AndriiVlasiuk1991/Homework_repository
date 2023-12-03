from django.shortcuts import render, redirect,  get_object_or_404
from .utils import get_mongodb
from django.core.paginator import Paginator
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Author, Quote
from django.contrib.auth.decorators import login_required
from bson.objectid import ObjectId
from django.urls import reverse
from django.db import connection

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={"quotes": quotes_on_page})

# def author_info(request, author_id):
#     db = get_mongodb()
#     author = db.authors.find_one({'_id': ObjectId(author_id)})
#     return render(request, 'quotes/author_info.html', context={"author": author})

def author_info(request, author_name):
    db = get_mongodb()
    author = db.authors.find_one({'fullname': author_name})
    return render(request, 'quotes/author_info.html', context={"author": author})


    
@login_required
def upload_quotes(request):
    form = QuoteForm()
    authors = Author.objects.all()
    tags = Tag.objects.all()
    db = get_mongodb()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            tag_ids = quote.tags.all() 

            tag_names = list(quote.tags.values_list('name', flat=True))
            db.quotes.insert_one({
                "quote":quote.quote,
                "author":quote.author.fullname,
                "tags":tag_names,
            })
            tags = request.POST.getlist('tags')
            if tags:
                quote.tags.set(tags)
            return redirect(to='quotes:root')  
    return render(request, 'quotes/upload_quotes.html', {'form': form, 'authors': authors, 'tags': tags})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})

@login_required
def author(request):
    db = get_mongodb()
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            db.authors.insert_one({
            'fullname': author.fullname,
            'born_date': author.born_date,
            'born_location': author.born_location,
            'description':author.description,
            })
            return redirect(to='quotes:root')  
    else:
        form = AuthorForm()

    return render(request, 'quotes/author.html', {'form': form})


