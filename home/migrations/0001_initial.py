# Generated by Django 5.0.6 on 2024-06-11 19:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('data_aquisicao', models.DateField()),
                ('quantidade', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cadastro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('data_reserva', models.DateTimeField(auto_now_add=True)),
                ('data_desejada', models.DateField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.produto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
