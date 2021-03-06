# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 12:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=10)),
                ('comment', models.CharField(blank=True, max_length=20)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes_models.Ingredient')),
                ('moment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes_models.Moment')),
            ],
            options={
                'verbose_name_plural': 'quantities',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('time', models.IntegerField()),
                ('source', models.TextField(blank=True)),
                ('category', models.ManyToManyField(to='recipes_models.Category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='TimeUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('seconds', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='time_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes_models.TimeUnit'),
        ),
        migrations.AddField(
            model_name='moment',
            name='ingredients',
            field=models.ManyToManyField(through='recipes_models.Quantity', to='recipes_models.Ingredient'),
        ),
        migrations.AddField(
            model_name='moment',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes_models.Recipe'),
        ),
    ]
