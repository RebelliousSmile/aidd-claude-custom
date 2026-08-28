# Python runtime strategies

| Signals | Local command class | Production concern |
| --- | --- | --- |
| Django | `manage.py runserver` through manager | WSGI/ASGI server, static collection, reviewed migrations |
| FastAPI | detected Uvicorn/Hypercorn entrypoint | ASGI process and worker count already chosen by project |
| Flask | detected Flask or WSGI entrypoint | WSGI process and application factory |
| Celery/RQ worker | separate worker command | independent process release and health proof |

Do not infer module names or server products solely from framework dependencies. Read configured entrypoints. Mixed or custom process managers are gaps until their commands are proven.

Persistent surfaces are facts per target, not framework defaults:

- Django migrations, Alembic revisions and equivalent versioned changes are `schema`.
- ORM rows, CMS/editorial records and queues are mutable `data`.
- Django storage files and user uploads are mutable `media`; collected static assets stay in the versioned code artifact.
- Local/object storage may be mirrored only to staging when listing, stable content hashes, resumable transfer and final verification are proven.
- S3, R2 or mounted volumes without those capabilities are a hard gap, not permission to upload an archive.

Production databases and media stores remain authoritative and independent for every federated instance.
