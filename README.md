# Spotify Clone by Elia Mirafiori

Hi! In this project I'll try to implement a clone of Spotify, complete in most of the engineering components.

Hope this will help someone!

## References

[FastAPI](https://fastapi.tiangolo.com/)
[SQLModel](https://sqlmodel.tiangolo.com/)
[Uvicorn](https://www.uvicorn.org/settings/)
[SQLite](https://sqlite.org/index.html)
[Alembic](https://alembic.sqlalchemy.org/en/latest/)
[PosgreSQL](https://www.postgresql.org/)
[NGINX](https://nginx.org/en/#basic_http_features)
[Docker](https://www.docker.com/resources/)
[Apache Kafka](https://kafka.apache.org/)
[MongoDB](https://www.mongodb.com/)
[Kubernetes](https://kubernetes.io/)

## Structure

```text
spotify_backend/
│
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── config.py              # App settings, env vars
│   ├── models/                # SQLModel(SQLAlchemy) models for PostgreSQL
│   ├── crud/                  # SQL-based business logic
│   ├── routers/               # Modular routers (auth, users, items, etc.)
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
