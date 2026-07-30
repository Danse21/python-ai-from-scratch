# Summer 2026: Python, Data Science & AI Training Documentation

This repository documents a self-motivated training program I undertook during the summer holidays to deepen my proficiency in Python, Data Science and AI. The curriculum ranges from core programming fundamentals to advanced AI applications in software development and bioinformatics.

Throughout this training, I used **Claude AI** for architectural design, structured guidance, and to generate real world exercises as well as get feedback from my solutions (acting as a senior developer).

Each folder contains solutions to exercises completed at the end of each module.

## Project:

### Title: Protein Function Prediction API

The core deliverable of this training is an API demonstrating real-world engineering practices, which predicts whether a protein seqence is a kinase or a protease, built entirely from scratch across several modules.

### Architecture

The Protein Function Prediction pipeline fetches protein sequences from the Uniprot REST API, generates embeddings using Meta's ESM-2 protein language model, trains a scikit-learn logistic regression classifier on those embeddings, and stores protein metadata in a local SQLite database (`biodata.db`).

### API Endpoints

- `GET ("/")` - health check, returns API status
- `GET ("/Protein/{uniprot_id}")` — Fetch a protein based on Uniprot accession ID from the local database
- `POST ("/protein")` — submits a protein sequence manually, validates that it only contains the 20 standard amino acids, and saves it to the database
- `POST ("/predict")` — accepts a protein sequence, generates an ESM-2 embedding, and returns a predicted class (kinase or protease) with a confidence score.

### Running Locally

```bash
cd Module_6_8_FastAPI
uvicorn async_endpoint:app --reload
or
uvicorn pydantic_schemas:app --reload
```

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Running with Docker

```bash
docker build -f Module_6_9_Docker/Dockerfile -t protein-api .
docker run -p 8000:8000 -v "$(pwd)/biodata.db:/app/biodata.db" protein-api
```

Or with Docker Compose from `Module_6_9_Docker/`:

```bash
docker compose up --build
```

### Continuous Integration

Every push to `main` and every pull request triggers a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs the full pytest suite before building the Docker image, so that broken code never gets containerized.

### Assumptions

- The classifier was trained on a small dataset (30 kinases + 30 proteases fetched from Uniprot), so predictions on sequences outside that training distribution may be unreliable.
- `DB_PATH` in `config.py` resolves relative to the project root; the SQLite database file must sit alongside `config.py`.
- The API expects raw, unmodified amino acid sequences using the 20 standard single-letter codes only.
- Retrieval quality has only been validated against a small, hand built 5-query test set; no validation yet against broader or heavily paraphrased queries.
- The Groq API for RAG and agent components require network access at runtime.
