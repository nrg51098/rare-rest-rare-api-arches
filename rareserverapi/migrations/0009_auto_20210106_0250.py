# Generated by Django 3.1.4 on 2021-01-06 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareserverapi', '0008_auto_20210106_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='reactions'
        ),
        migrations.AddField(
            model_name='post',
            name='reactions',
            field=models.ManyToManyField(
                related_name='reaction_posts', related_query_name='reaction_post', to='rareserverapi.PostReactions'),
        ),
    ]
