# Generated by Django 5.1.7 on 2025-05-29 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BiblioApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='tags',
            field=models.ManyToManyField(blank=True, through='BiblioApp.ReferenceTag', to='BiblioApp.tag'),
        ),
    ]
