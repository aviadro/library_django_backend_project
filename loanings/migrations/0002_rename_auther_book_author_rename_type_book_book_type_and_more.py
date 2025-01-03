# Generated by Django 5.1.2 on 2024-10-31 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='auther',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='type',
            new_name='book_type',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
