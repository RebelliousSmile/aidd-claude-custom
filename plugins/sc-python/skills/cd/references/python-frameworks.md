# Python runtime strategies

| Signals | Local command class | Production concern |
| --- | --- | --- |
| Django | `manage.py runserver` through manager | WSGI/ASGI server, static collection, reviewed migrations |
| FastAPI | detected Uvicorn/Hypercorn entrypoint | ASGI process and worker count already chosen by project |
| Flask | detected Flask or WSGI entrypoint | WSGI process and application factory |
| Celery/RQ worker | separate worker command | independent process release and health proof |

Do not infer module names or server products solely from framework dependencies. Read configured entrypoints. Mixed or custom process managers are gaps until their commands are proven.
