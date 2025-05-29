from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReferenceForm
from .models import Collection, Reference
from django.contrib.auth.forms import UserCreationForm

@login_required
def home(request):
    user_collections = Collection.objects.filter(owner=request.user)
    return render(request, 'BiblioApp/home.html', {'collections': user_collections})

@login_required
def add_collection(request):
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

        return redirect('BiblioApp:home')

    user_references = Reference.objects.filter(owner=request.user)
    return render(request, 'BiblioApp/add_collection.html', {'references': user_references})

@login_required
def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, owner=request.user)
    references = collection.references.all()
    return render(request, 'BiblioApp/view_collection.html', {
        'collection': collection,
        'references': references,
    })

@login_required
def create_reference(request):
    if request.method == 'POST':
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.owner = request.user
            reference.save()
            form.save_m2m()
            return redirect('BiblioApp:reference_list')
    else:
        form = ReferenceForm()
    return render(request, 'BiblioApp/create_reference.html', {'form': form})

@login_required
def edit_reference(request, reference_id):
    reference = get_object_or_404(Reference, id=reference_id, owner=request.user)
    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            return redirect('BiblioApp:reference_list')
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'BiblioApp/edit_reference.html', {'form': form, 'reference': reference})

@login_required
def delete_reference(request, reference_id):
    reference = get_object_or_404(Reference, id=reference_id, owner=request.user)
    if request.method == 'POST':
        reference.delete()
        return redirect('BiblioApp:reference_list')
    return render(request, 'BiblioApp/delete_reference.html', {'reference': reference})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('BiblioApp:login')
    else:
        form = UserCreationForm()
    return render(request, 'BiblioApp/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'BiblioApp/profile.html')

@login_required
def dashboard(request):
    return render(request, 'BiblioApp/dashboard.html')

@login_required
def reference_list(request):
    references = Reference.objects.filter(owner=request.user)
    return render(request, 'BiblioApp/reference_list.html', {'references': references})
