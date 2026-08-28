# Python SQL delivery

Application artifacts, schema migrations and mutable data are separate operations.

- Django uses the project's `manage.py migrate` plan/check before applying reviewed migrations.
- SQLAlchemy uses the already configured migration tool, commonly Alembic; the ORM dependency alone is not evidence of a migration command.
- `deploy:db` may apply reviewed forward migrations with backup and recovery. It does not mean copying a local database.
- Production permits reviewed schema migration, but refuses local-to-production mutable data transfer regardless of confirmation.
- Staging may mirror scoped local data only when its contract declares local authority, a reliable inventory/diff strategy, quiescence where required, fresh backup, stable preview, explicit confirmation, proof and recovery.
- Production-to-local and every target-to-target copy are outside this CD contract and must be refused.

Workers must not race schema changes: the release procedure declares ordering and compatibility.
