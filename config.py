import os

# Always points to project root regardless of where script is run from
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, "biodata.db")
