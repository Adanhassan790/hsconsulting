# Generated migration to make logo and favicon optional

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_coresettings_facebook_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coresettings',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='branding/'),
        ),
        migrations.AlterField(
            model_name='coresettings',
            name='favicon',
            field=models.ImageField(blank=True, null=True, upload_to='branding/'),
        ),
    ]
