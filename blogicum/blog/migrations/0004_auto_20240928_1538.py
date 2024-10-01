# Generated by Django 3.2.16 on 2024-09-28 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240925_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('created_at',)},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='autor',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commetns', to='blog.post'),
        ),
    ]
