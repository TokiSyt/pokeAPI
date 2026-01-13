from django.db import migrations


def recreate_m2m_table(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor

    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS generations_generation_allowed_users;")

    if vendor == "sqlite":
        sql = """
            CREATE TABLE generations_generation_allowed_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation_id BIGINT NOT NULL REFERENCES generations_generation(id) DEFERRABLE INITIALLY DEFERRED,
                customuser_id BIGINT NOT NULL REFERENCES accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED
            );
        """
    else:
        sql = """
            CREATE TABLE generations_generation_allowed_users (
                id BIGSERIAL PRIMARY KEY,
                generation_id BIGINT NOT NULL REFERENCES generations_generation(id) DEFERRABLE INITIALLY DEFERRED,
                customuser_id BIGINT NOT NULL REFERENCES accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED
            );
        """

    with connection.cursor() as cursor:
        cursor.execute(sql)


def reverse_recreate(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS generations_generation_allowed_users;")


class Migration(migrations.Migration):
    dependencies = [
        ("generations", "0002_create_m2m_table"),
    ]

    operations = [
        migrations.RunPython(recreate_m2m_table, reverse_recreate),
    ]
