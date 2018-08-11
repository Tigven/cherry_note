# Generated by Django 2.0.8 on 2018-08-11 09:27

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.IntegerField(default=0, verbose_name='Offset')),
                ('justification', models.CharField(choices=[('LT', 'left'), ('RT', 'right'), ('CR', 'center')], default='LT', max_length=2)),
                ('code', models.TextField(blank=True, default='', verbose_name='Code')),
                ('syntax', models.CharField(choices=[('PY2', 'python2'), ('PY3', 'python3')], max_length=4)),
                ('width', models.IntegerField(default=700, verbose_name='Width')),
                ('height', models.IntegerField(default=100, verbose_name='Height')),
                ('show_line_no', models.BooleanField(default=False, verbose_name='Show line numbers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.IntegerField(default=0, verbose_name='Offset')),
                ('justification', models.CharField(choices=[('LT', 'left'), ('RT', 'right'), ('CR', 'center')], default='LT', max_length=2)),
                ('name', models.CharField(max_length=1024, verbose_name='File name')),
                ('url', models.CharField(max_length=1024, verbose_name='File URL')),
                ('size', models.IntegerField(default=0, verbose_name='Size')),
                ('info', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, verbose_name='Extra info')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Note name')),
                ('content', models.TextField(blank=True, default='', verbose_name='Note content')),
                ('syntax', models.CharField(choices=[('CU', 'custom'), ('SI', 'simple')], default='SI', max_length=2)),
                ('is_read_only', models.BooleanField(default=False, verbose_name='Read only')),
                ('has_code_box', models.BooleanField(default=False, verbose_name='Has code box')),
                ('has_table', models.BooleanField(default=False, verbose_name='Has table')),
                ('has_image', models.BooleanField(default=False, verbose_name='Has image')),
                ('has_file', models.BooleanField(default=False, verbose_name='Has file')),
                ('level', models.IntegerField(default=0, verbose_name='Level')),
                ('ts_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('ts_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('children', models.ManyToManyField(blank=True, null=True, related_name='_note_children_+', to='notes.Note', verbose_name='Child notes')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='notes.Note', verbose_name='Parent note')),
            ],
            options={
                'ordering': ('ts_created',),
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.IntegerField(default=0, verbose_name='Offset')),
                ('justification', models.CharField(choices=[('LT', 'left'), ('RT', 'right'), ('CR', 'center')], default='LT', max_length=2)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, verbose_name='Table content')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='notes.Note', verbose_name='Note')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Tag name')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='notes.Note', verbose_name='Note'),
        ),
        migrations.AddField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='codebox',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='notes.Note', verbose_name='Note'),
        ),
    ]
