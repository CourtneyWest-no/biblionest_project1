from django.contrib import admin
from .models import CustomUser, Reference, Collection, CollectionReference, Tag, ReferenceTag

admin.site.register(CustomUser)
admin.site.register(Reference)
admin.site.register(Collection)
admin.site.register(CollectionReference)
admin.site.register(Tag)
admin.site.register(ReferenceTag)


