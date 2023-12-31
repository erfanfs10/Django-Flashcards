# Generated by Django 4.2 on 2023-10-29 15:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('front', models.TextField()),
                ('back', models.TextField()),
                ('us_pronunciation', models.FileField(default='undefined.aac', upload_to='words_us_pronunciation')),
                ('uk_pronunciation', models.FileField(default='undefined.aac', upload_to='words_uk_pronunciation')),
                ('correct_counts', models.PositiveSmallIntegerField(default=0)),
                ('incorrect_counts', models.PositiveSmallIntegerField(default=0)),
                ('review_counts', models.PositiveSmallIntegerField(default=0)),
                ('box_number', models.PositiveSmallIntegerField(default=1)),
                ('next_review', models.DateTimeField(default=django.utils.timezone.now)),
                ('learned', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='category.category')),
            ],
        ),
    ]
