# Generated by Django 2.2.1 on 2019-05-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190517_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='date in invoice')),
                ('date_creation', models.DateTimeField(verbose_name='date creation in system')),
                ('invoice_capture', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
