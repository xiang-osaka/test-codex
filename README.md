# test-codex

This repository contains a minimal example membership registration app.

## Running the server

The application is implemented in `app.py` and uses Python's built-in
`http.server` module along with SQLite for storage. To start the server run:

```bash
python3 app.py
```

By default the server listens on port `8000` and creates a local
`members.db` SQLite database if it does not exist.

### Registering a new member

Send a POST request to `/register` with JSON body containing `name` and
`contact` fields.

Example using `curl`:

```bash
curl -X POST http://localhost:8000/register \
    -H 'Content-Type: application/json' \
    -d '{"name": "Alice", "contact": "alice@example.com"}'
```

### Listing all members

Send a GET request to `/members` to retrieve all registered members:

```bash
curl http://localhost:8000/members
```
