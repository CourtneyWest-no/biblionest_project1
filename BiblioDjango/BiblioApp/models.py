from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="biblioapp_users",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="biblioapp_users_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Reference(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField(null=True, blank=True)
    source = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, through='ReferenceTag', blank=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


class Collection(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    references = models.ManyToManyField(Reference, through='CollectionReference')

    def __str__(self):
        return self.name


class CollectionReference(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collection', 'reference')


class ReferenceTag(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('reference', 'tag')

