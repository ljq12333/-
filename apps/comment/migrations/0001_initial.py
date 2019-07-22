# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storm', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(max_length=100, default=False)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(to='storm.Article')),
                ('author', models.ForeignKey(to='storm.Blog_User')),
            ],
            options={
                'verbose_name': '用户评论',
                'verbose_name_plural': '用户评论',
                'db_table': 'comment',
                'ordering': ['-comment_date'],
            },
        ),
    ]
