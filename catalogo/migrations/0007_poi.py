# Generated by Django 4.0.4 on 2022-06-20 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0006_alter_ejemplar_options_alter_ejemplar_isbn_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='POI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
            ],
        ),
    ]
