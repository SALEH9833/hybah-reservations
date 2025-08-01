# Generated by Django 5.2.4 on 2025-07-27 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='photos_services/')),
                ('ordre', models.IntegerField(default=0, help_text='Permet de trier les services (le plus petit en premier)')),
            ],
            options={
                'ordering': ['ordre'],
            },
        ),
    ]
