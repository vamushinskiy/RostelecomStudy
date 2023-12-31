# Generated by Django 4.2.7 on 2024-01-07 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_article_options_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('view_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='news.article')),
            ],
            options={
                'ordering': ('-view_date',),
                'indexes': [models.Index(fields=['-view_date'], name='news_viewco_view_da_c81d57_idx')],
            },
        ),
    ]
