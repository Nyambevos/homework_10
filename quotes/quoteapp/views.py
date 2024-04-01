from django.shortcuts import render, redirect

from .forms import AuthorForm

# Create your views here.

def main(request):
    return render(request, 'quoteapp/index.html')

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