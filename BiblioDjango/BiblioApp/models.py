from django.contrib.auth.models import AbstractUser
from django.db import models

### 1. Custom User Model ###
class CustomUser(AbstractUser):
    """Extends Django's built-in User model for future flexibility"""
    email = models.EmailField(unique=True)

     # Fix the conflict by setting unique related_name values
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="biblioapp_users",  # Custom related name to prevent clashes
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="biblioapp_users_permissions",  # Custom related name to prevent clashes
        blank=True,
    )

    def __str__(self):
        return self.username
    
    ### 2. Reference Model ###
class Reference(models.Model):
    """Stores bibliographic records"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField(null=True, blank=True)
    source = models.URLField(blank=True, null=True)  # DOI, journal link, etc.
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author}"
    
    ### 3. Collection Model ###
class Collection(models.Model):
    """Users can group references into collections"""
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    references = models.ManyToManyField(Reference, through='CollectionReference')

    def __str__(self):
        return self.name
    
    ### 4. Intermediate Model for Many-to-Many (Collection - Reference) ###
class CollectionReference(models.Model):
    """Intermediate table for many-to-many relationship between Collection and Reference"""
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)  # Timestamp when added

    class Meta:
        unique_together = ('collection', 'reference')  # Prevent duplicate references in a collection

        ### 5. Tag Model ###
class Tag(models.Model):
    """Stores unique tags for references"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    ### 6. Intermediate Model for Many-to-Many (Reference - Tag) ###
class ReferenceTag(models.Model):
    """Many-to-Many table linking References with Tags"""
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('reference', 'tag')  # Prevent duplicate tags on a reference
