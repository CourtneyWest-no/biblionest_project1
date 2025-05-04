from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ReferenceForm
from .models import Collection, Reference
from django.http import HttpResponse

@login_required
def home(request):
    """Home page view, accessible only to logged-in users."""
    user_collections = Collection.objects.filter(owner=request.user)  
    return render(request, 'BiblioApp/home.html', {'collections': user_collections})

@login_required
def add_collection(request):
    """View to add a new collection and optionally add references."""
    if request.method == 'POST':
        collection_name = request.POST.get('collection_name')
        references_ids = request.POST.getlist('references')  

        collection = Collection.objects.create(name=collection_name, owner=request.user)

        existing_references = Reference.objects.filter(id__in=references_ids, owner=request.user)
        collection.references.add(*existing_references)

        new_titles = request.POST.getlist('new_references_title[]')
        new_authors = request.POST.getlist('new_references_author[]')
        new_publication_dates = request.POST.getlist('new_references_publication_date[]')
        new_sources = request.POST.getlist('new_references_source[]')

        for title, author, publication_date, source in zip(new_titles, new_authors, new_publication_dates, new_sources):
            if title.strip() and author.strip():  
                new_reference = Reference.objects.create(
                    title=title.strip(),
                    author=author.strip(),
                    publication_date=publication_date or None,
                    source=source or None,
                    owner=request.user
                )
                collection.references.add(new_reference)

        return redirect('home')

    user_references = Reference.objects.filter(owner=request.user) 
    return render(request, 'BiblioApp/add_collection.html', {'references': user_references})