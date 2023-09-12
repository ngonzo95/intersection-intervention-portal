# Generated by Django 4.2.4 on 2023-08-02 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Intersection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(db_index=True, decimal_places=16, max_digits=20)),
                ('lon', models.DecimalField(db_index=True, decimal_places=16, max_digits=20)),
                ('cluster_id', models.IntegerField()),
                ('intersection_type', models.CharField(db_index=True, max_length=80)),
                ('number_of_accidents', models.IntegerField(db_index=True)),
                ('fatal_accident_number', models.IntegerField(db_index=True)),
                ('major_accident_number', models.IntegerField(db_index=True)),
                ('minor_accident_number', models.IntegerField()),
                ('unknown_accident_number', models.IntegerField()),
                ('property_accident_number', models.IntegerField()),
                ('average_cost_to_insurers', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_intersection_type', models.CharField(db_index=True, max_length=80)),
                ('conversion_cost', models.DecimalField(db_index=True, decimal_places=2, max_digits=20)),
                ('accident_reduction_rate', models.DecimalField(decimal_places=8, max_digits=10)),
                ('accident_severity_reduction_rate', models.DecimalField(decimal_places=8, max_digits=10)),
                ('intersection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_app.intersection')),
            ],
        ),
    ]
