# Spotify Clone by Elia Mirafiori

Hi! In this project I'll try to implement a clone of Spotify, complete in most of the engineering components.

Hope this will help someone!

## Structure

```text
spotify_backend/
│
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── config.py              # App settings, env vars
│   ├── deps/                  # Dependencies for routes (auth, db, etc.)
│   ├── models/                # SQLModel(SQLAlchemy) models for PostgreSQL
│   ├── schemas/               # SQLModel(Pydantic) schemas
│   ├── crud/                  # SQL-based business logic
│   ├── services/              # Core services (auth, recs, etc.)
│   ├── api/
│   │   ├── routes/            # Modular routers (auth, users, items, etc.)
│   │   └── deps.py            # API-layer dependencies
│   ├── mongo/                 # MongoDB access layer
│   │   ├── client.py
│   │   └── trackers.py        # Behavior tracking (e.g., clicks, views)
│   └── recommender/
│       ├── batch.py           # Entry point for batch jobs
│       ├── pipeline.py        # Data loading, feature engineering, model
│       └── utils.py           # Helpers
│
├── scripts/                   # CLI tools or one-off scripts
│   └── populate_demo_data.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── recommender/
│
├── alembic/                   # DB migrations
│
├── .env
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```
