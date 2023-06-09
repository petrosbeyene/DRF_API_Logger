# Generated by Django 4.2 on 2023-04-27 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="APIRequestLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("path", models.CharField(max_length=255)),
                ("method", models.CharField(max_length=10)),
                ("status_code", models.IntegerField()),
                ("request_data", models.JSONField(null=True)),
                ("response_data", models.JSONField(null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
    ]
