# Generated by Django 4.1.3 on 2022-12-04 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20221202_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataScheme',
            fields=[
                ('scheme_id', models.AutoField(primary_key=True, serialize=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='DataSchemeColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('datatype', models.CharField(choices=[('Full name', 'Full name'), ('Job', 'Job'), ('Domain name', 'Domain name'), ('Company name', 'Company name'), ('Address', 'Address')], max_length=15)),
                ('datascheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.datascheme')),
            ],
        ),
    ]
