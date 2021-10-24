# Generated by Django 3.2.7 on 2021-10-20 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Тех.обслуживание'), ('o', 'Выдан'), ('a', 'Доступен'), ('r', 'Забронированный')], default='m', help_text='Статус книги', max_length=1),
        ),
    ]