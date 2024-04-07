from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag, Quote

# Create your views here.

def main(request):
    quotes_list = list(Quote.objects.select_related('author'))
    if quotes_list:
        paginator = Paginator(quotes_list, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'quoteapp/index.html', {'page_obj': page_obj, 'top_tags': get_top_tags()})
    else:
        return redirect(to='parser:main')

@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})
    else:
        return render(request, 'quoteapp/author.html', {'form': AuthorForm()})

@login_required  
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})

@login_required
def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.get(fullname__in=request.POST.getlist('author'))
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, "form": form})
    return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, "form": QuoteForm()})

def detail_author(request, slug_author):
    author = get_object_or_404(Author, slug=slug_author)
    return render(request, 'quoteapp/detail_author.html', {"author": author})

def quotes_by_tag(request, tag):
    quotes_list = list(Quote.objects.filter(tags__name=tag).select_related('author'))
    paginator = Paginator(quotes_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'quoteapp/index.html', {'page_obj': page_obj, 'top_tags': get_top_tags()})

def get_top_tags():
    top_tags_list = []
    top_tags = Quote.objects.values('tags').annotate(count=Count('tags')).order_by('-count')[:10]
    for item in top_tags:
        tag = Tag.objects.get(id=item['tags'])
        top_tags_list.append(tag.name)
    return top_tags_list