from django.db import migrations, models


def load_initial_data(apps, schema_editor):
    Sites = apps.get_model('database', 'Sites')
    initial_sites = [
        'http://openphish.com/feed.txt',
    ]
    for site in initial_sites:
        Sites.objects.create(url=site)


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True))
            ],
        ),
        migrations.CreateModel(
            name='MalwareSites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True))
            ],
        ),
        migrations.CreateModel(
            name='PhishingSites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True))
            ],
        ),
        migrations.RunPython(load_initial_data),
    ]
