# Generated by Django 4.2.9 on 2024-08-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_rename_contect_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
