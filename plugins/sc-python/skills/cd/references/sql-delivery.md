# Python SQL delivery

Application artifacts, schema migrations and mutable data are separate operations.

- Django uses the project's `manage.py migrate` plan/check before applying reviewed migrations.
- SQLAlchemy uses the already configured migration tool, commonly Alembic; the ORM dependency alone is not evidence of a migration command.
- `deploy:db` may apply reviewed forward migrations with backup and recovery. It does not mean copying a local database.
- Any local-to-production data import requires named scope, fresh production backup, dry-run/review, explicit confirmation, proof and recovery.
- A production-to-local copy is a distinct `pull:*` command with local-overwrite protection.

Workers must not race schema changes: the release procedure declares ordering and compatibility.
