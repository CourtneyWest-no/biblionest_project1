from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import ReferenceForm
from .models import Collection, Reference, Tag


@login_required
def home(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'BiblioApp/home.html', {'collections': collections})

@login_required
def add_collection(request):
    if request.method == 'POST':
        collection_name = request.POST.get('collection_name')
        reference_ids = request.POST.getlist('references')
        collection = Collection.objects.create(name=collection_name, owner=request.user)
        existing_references = Reference.objects.filter(id__in=reference_ids, owner=request.user)
        collection.references.add(*existing_references)

        titles = request.POST.getlist('new_references_title[]')
        authors = request.POST.getlist('new_references_author[]')
        publication_dates = request.POST.getlist('new_references_publication_date[]')
        sources = request.POST.getlist('new_references_source[]')

        for title, author, pub_date, source in zip(titles, authors, publication_dates, sources):
            if title.strip() and author.strip():
                new_ref = Reference.objects.create(
                    title=title.strip(),
                    author=author.strip(),
                    publication_date=pub_date or None,
                    source=source or None,
                    owner=request.user
                )
                collection.references.add(new_ref)

        return redirect('BiblioApp:home')

    references = Reference.objects.filter(owner=request.user)
    return render(request, 'BiblioApp/add_collection.html', {'references': references})

@login_required
def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, owner=request.user)
    references = collection.references.all()
    return render(request, 'BiblioApp/view_collection.html', {
        'collection': collection,
        'references': references
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

            new_tags = form.cleaned_data.get('new_tags')
            if new_tags:
                for tag_name in new_tags.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        reference.tags.add(tag)

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

            new_tags = form.cleaned_data.get('new_tags')
            if new_tags:
                for tag_name in new_tags.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        reference.tags.add(tag)

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

@login_required
def reference_list(request):
    references = Reference.objects.filter(owner=request.user)
    return render(request, 'BiblioApp/reference_list.html', {'references': references})

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
