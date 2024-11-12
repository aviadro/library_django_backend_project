# Generated by Django 5.1.2 on 2024-11-01 07:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanings', '0003_loan_due_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='cust_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL),
        ),
    ]