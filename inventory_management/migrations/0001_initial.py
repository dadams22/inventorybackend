# Generated by Django 3.0.6 on 2020-05-22 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_measurement', models.FloatField()),
                ('last_measurement_timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('associated_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_management.InventoryItem')),
                ('associated_site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_management.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory_management.Scale')),
            ],
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='associated_site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_management.Site'),
        ),
    ]
