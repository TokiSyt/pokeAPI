from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('generations', '0002_create_m2m_table'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DROP TABLE IF EXISTS generations_generation_allowed_users;

                CREATE TABLE generations_generation_allowed_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    generation_id BIGINT NOT NULL REFERENCES generations_generation(id) DEFERRABLE INITIALLY DEFERRED,
                    customuser_id BIGINT NOT NULL REFERENCES accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED
                );
            """,
            reverse_sql="""
                DROP TABLE IF EXISTS generations_generation_allowed_users;
            """
        )
    ]
