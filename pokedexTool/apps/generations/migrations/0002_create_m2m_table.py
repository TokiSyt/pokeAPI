from django.db import migrations


def create_m2m_table(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor

    if vendor == "sqlite":
        sql = """
            CREATE TABLE IF NOT EXISTS generations_generation_allowed_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation_id BIGINT NOT NULL REFERENCES generations_generation(id) DEFERRABLE INITIALLY DEFERRED,
                user_id BIGINT NOT NULL REFERENCES accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED
            );
        """
    else:
        sql = """
            CREATE TABLE IF NOT EXISTS generations_generation_allowed_users (
                id BIGSERIAL PRIMARY KEY,
                generation_id BIGINT NOT NULL REFERENCES generations_generation(id) DEFERRABLE INITIALLY DEFERRED,
                user_id BIGINT NOT NULL REFERENCES accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED
            );
        """

    with connection.cursor() as cursor:
        cursor.execute(sql)


def drop_m2m_table(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS generations_generation_allowed_users;")


class Migration(migrations.Migration):
    dependencies = [
        ("generations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_m2m_table, drop_m2m_table),
    ]
