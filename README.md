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

## Build and Run the project

### PostgreSQL

```bash
docker run -d \
  --name my-postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -v my_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

#### Breakdown of the Command

- `-d`: Run the container in detached mode (in the background).

- `--name my-postgres`: Assign a name to the container for easier management.

- `-e POSTGRES_USER=myuser`: Set the default PostgreSQL user to myuser.

- `-e POSTGRES_PASSWORD=mypassword`: Set the password for the default user.

- `-e POSTGRES_DB=mydatabase`: Create a default database named mydatabase.

- `-v my_postgres_data:/var/lib/postgresql/data`: Mount a named volume my_postgres_data to persist database data across container restarts.

- `-p 5432:5432`: Expose PostgreSQL's default port 5432 to the host machine, allowing external connections.

- `postgres`: Use the official PostgreSQL image from Docker Hub.

When you create a named volume in Docker, such as `my_postgres_data`, Docker manages its storage location.

In Linux by default, Docker stores volumes in the directory `/var/lib/docker/volumes/`. For a volume named `my_postgres_data`, the data would typically be located at `/var/lib/docker/volumes/my_postgres_data/_data`.

### FastAPI

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
version: "3.8"

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
version: "3.8"

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

### [`pgvector`](https://github.com/pgvector/pgvector?tab=readme-ov-file#docker)

Step 1: Connect to Your PostgreSQL Container

First, identify the name or ID of your running PostgreSQL container:

```bash
docker ps
```

Once identified, access the container's shell:

```bash
docker exec -it <container_name_or_id> bash
```

Step 2: Install `pgvector`

```bash
apt update && apt install postgresql-17-pgvector
```

_Note: Replace `17` with your Postgres server version_

Step 3: Add the pgvector Extension

Then, connect to the PostgreSQL database using the `psql` command-line tool:

```bash
psql -d my_dababase_name -U my_username -W my_username_password
```

Replace `my_username` with your PostgreSQL username if it's different.

```sql
CREATE EXTENSION vector;
```

Step 4: Verify the Installation

After installation, you can confirm that the extension is active by running the query:

```bash
SELECT * FROM pg_extension WHERE extname = 'vector';
```

To use UUIDs as identifiers in a FastAPI application with PostgreSQL, you can leverage SQLAlchemy or SQLModel. Here's how to implement UUIDs effectively in both approaches:([medium.com][1])

### Using SQLModel with UUIDs

#### 1. Define a UUID Field

In your model, define a UUID field using `uuid.UUID` and `Field`:

```python
import uuid
from sqlmodel import SQLModel, Field
from uuid import UUID

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
```

This ensures that each `User` record has a unique UUID as its primary key.

#### 2. Enable PostgreSQL UUID Generation (Optional)

For automatic UUID generation on the database side, you can use PostgreSQL's `gen_random_uuid()` function. Ensure the `pgcrypto` extension is enabled:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

Then, set the default value for the UUID column:

```python
from sqlalchemy import func

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True, sa_column_kwargs={"server_default": func.gen_random_uuid()})
    name: str
```

This approach offloads UUID generation to PostgreSQL, which can be more efficient.

#### 🧪 Example: FastAPI with SQLAlchemy and UUIDs

Here's a complete example integrating FastAPI with SQLAlchemy and UUIDs:

```python
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/")
def create_user(name: str, db: Session = Depends(get_db)):
    db_user = User(name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

This setup allows you to create users with UUIDs as their primary keys.

---

#### 🔄 Migrating Existing Data to UUIDs

If you're migrating from integer-based IDs to UUIDs, follow these steps:

1. **Add a new UUID column**:

   ```sql
   ALTER TABLE users ADD COLUMN id_new UUID;
   ```

2. **Populate the new column**:

   ```sql
   UPDATE users SET id_new = gen_random_uuid();
   ```

3. **Set the new column as primary key**:

   ```sql
   ALTER TABLE users DROP CONSTRAINT users_pkey;
   ALTER TABLE users ADD PRIMARY KEY (id_new);
   ```

4. **Remove the old column**:

   ```sql
   ALTER TABLE users DROP COLUMN id;
   ALTER TABLE users RENAME COLUMN id_new TO id;
   ```

Ensure you test these steps in a development environment before applying them to production.

#### Summary

- **SQLAlchemy**: Use `UUID(as_uuid=True)` for UUID columns. Optionally, set `server_default=func.gen_random_uuid()` for automatic UUID generation by PostgreSQL.

- **SQLModel**: Use `Field(default_factory=uuid.uuid4)` for UUID fields. Optionally, set `sa_column_kwargs={"server_default": func.gen_random_uuid()}` for automatic UUID generation by PostgreSQL.

- **Migration**: Follow the steps above to migrate existing data to UUIDs.
