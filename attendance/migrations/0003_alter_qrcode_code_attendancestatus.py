# Generated by Django 4.0.3 on 2022-03-10 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0002_alter_attendancelog_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='code',
            field=models.CharField(blank=True, default='105988a3321cf19c1d97b31f8b7b0ec4', max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='AttendanceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('TIMEIN', 'time in'), ('TIMEOUT', 'time out')], default='TIMEIN', max_length=10)),
                ('date_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]