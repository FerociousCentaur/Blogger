# Generated by Django 3.2 on 2021-04-13 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='images/')),
                ('rating', models.CharField(blank=True, max_length=3)),
                ('published', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField()),
                ('commentOn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='commentOn', to='Blog.article')),
            ],
        ),
    ]
