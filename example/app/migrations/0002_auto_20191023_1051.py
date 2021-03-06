# Generated by Django 2.2.5 on 2019-10-23 10:51

import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grapesjsjsonmodel',
            name='url',
        ),
        migrations.AddField(
            model_name='grapesjsjsonmodel',
            name='domain',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='grapesjsjsonmodel',
            name='path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='grapesjsjsonmodel',
            name='gjs_assets',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grapesjsjsonmodel',
            name='gjs_components',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grapesjsjsonmodel',
            name='gjs_css',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grapesjsjsonmodel',
            name='gjs_html',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grapesjsjsonmodel',
            name='gjs_styles',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True),
        ),
    ]
