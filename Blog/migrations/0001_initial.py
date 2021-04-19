# Generated by Django 3.2 on 2021-04-19 00:36

from django.db import migrations, models
import uuid


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
                ('aid', models.UUIDField(default=uuid.uuid4, editable=False)),
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
                ('cid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('commentText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
                ('msg', models.TextField()),
            ],
        ),
    ]
