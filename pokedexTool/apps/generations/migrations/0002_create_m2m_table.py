from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('generations', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS generations_generation_allowed_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    generation_id BIGINT NOT NULL REFERENCES generations_generation(id) DEFERRABLE INITIALLY DEFERRED,
                    user_id BIGINT NOT NULL REFERENCES accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS generations_generation_allowed_users;"
        )
    ]
