from django.shortcuts import render, redirect

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote


# Create your views here.

def index(request):
    return render(request, 'authors/index.html', context={"msg": "Hello word!"})


def authors(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            new_author = form.save()

            new_author.save()
            return redirect(to='authors:authors')
        else:
            return render(request, 'authors/authors.html', context={"form": form})
    return render(request, 'authors/authors.html', context={"form": AuthorForm(instance=Author())})


def quotes(request):
    # form = QuoteForm(instance=Quote())
    authors = Author.objects.all()
    tags = Tag.objects.all()
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Quote())

        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.save()
            return redirect(to='authors:quotes')
        else:
            return render(request, "authors/quotes.html", context={"authors": authors, "tags": tags, "form": form})

    return render(request, "authors/quotes.html", context={"authors": authors, "tags": tags, "form": QuoteForm(instance=Quote())})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST, instance=Tag())
        if form.is_valid():
            tag = form.save()

            tag.save()
            return redirect(to='authors:tag')
        else:
            return render(request, 'authors/tag.html', context={'form': form})
    return render(request, 'authors/tag.html', context={'form': TagForm(instance=Tag())})
