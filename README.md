# Spotify Clone by Elia Mirafiori

Hi! In this project I'll try to implement a clone of Spotify, complete in most of the engineering components.

Hope this will help someone!

## References

[Template Reference](https://github.com/fastapi/full-stack-fastapi-template)
[FastAPI](https://fastapi.tiangolo.com/)
[FastAPI - Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
[SQLModel](https://sqlmodel.tiangolo.com/)
[Uvicorn](https://www.uvicorn.org/settings/)
[SQLite](https://sqlite.org/index.html)
[Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
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

## Build and Run the project

By default, Uvicorn binds to `127.0.0.1`, which is only accessible from within the container. To make your FastAPI app accessible from outside the container, you need to bind it to `0.0.0.0`.

Run the following command to create the Docker Image:

```bash
docker build -t spotify_clone:test .
```

The last "." specify the location of the Dockerfile.

Run the following command to create the Docker Container:

```bash
docker run --rm -p 8000:8000 spotify_clone:test
```

The "-p" flag specifies the port to be mapped "-p host_port:container_port".

If a VOLUME is needed, mount it using the `-v` syntax:

```bash
docker run -d \
  -p 8000:8000 \
  -v /home/user/projects/fastapi-app:/app \
  spotify_clone
```

Or using the `--mount` syntax:

```bash
docker run -d \
  -p 8000:8000 \
  --mount type=bind,source=/path/on/host,target=/path/in/container \
  spotify_clone
```

If you are using a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  fastapi:
    image: spotify_clone
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
```

In this configuration, the `./app` directory on your host is mounted to `/app` in the container.

**NOTE:**
It's important to note that you cannot specify bind mounts directly within a `Dockerfile`. The `Dockerfile` is designed to define the image's contents and configuration, not how it interacts with the host system at runtime. This design choice ensures that Docker images remain portable and not tied to specific host configurations.

While the `VOLUME` instruction in a `Dockerfile` can declare a mount point, it doesn't allow you to specify a host directory for a bind mount. Instead, it creates an anonymous volume managed by Docker.

For example:

```Dockerfile
VOLUME /app/data
```

This indicates that `/app/data` should be a volume. When a container is created from this image, Docker will create an anonymous volume unless you specify one.

If you are using a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  fastapi:
    image: myfastapiapp
    ports:
      - "8000:8000"
    volumes:
      - my_volume:/app/data

volumes:
  my_volume:
```

This configuration mounts the `my_volume` to `/app/data` in the `fastapi` service.

The `my_volume` is mounted to the `/app/data` directory inside the `fastapi` service container. This setup ensures that any data written to `/app/data` within the container is stored in the `my_volume` volume on the host system. This approach is beneficial for persisting data across container restarts and recreations.
