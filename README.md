
To install backend dependencies:
* Install poetry
* run `poetry install` in the root directory


To start the backend locally:
```terminal
poetry run uvicorn backend.api:app --host=0.0.0.0 --port=${PORT}
```

