# Generated by Django 2.2.3 on 2019-07-11 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0002_roominfo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('room_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.RoomInfo')),
            ],
        ),
    ]
