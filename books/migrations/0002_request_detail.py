# Generated by Django 3.2 on 2021-04-23 14:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='request_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_date', models.DateField(default=datetime.datetime(2021, 4, 30, 14, 19, 35, 363626, tzinfo=utc))),
                ('request_status', models.CharField(default='Pending', max_length=15)),
                ('book_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
