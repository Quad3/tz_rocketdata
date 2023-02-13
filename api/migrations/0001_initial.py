# Generated by Django 4.1.6 on 2023-02-13 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('house_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.address')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('level', models.IntegerField()),
                ('debt', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.contact')),
                ('products', models.ManyToManyField(to='api.product')),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.producer')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producer')),
            ],
        ),
    ]
