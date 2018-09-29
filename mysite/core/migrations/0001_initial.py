# Generated by Django 2.1.1 on 2018-09-29 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('restaurantId', models.CharField(max_length=100)),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
            ],
        ),
    ]
