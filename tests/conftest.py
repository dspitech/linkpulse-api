"""Configuration pytest : isole les tests dans leur propre base SQLite
et nettoie la table 'links' avant chaque test pour garantir l'independance
des tests entre eux.
"""
import os
os.environ["DB_PATH"] = "test_linkpulse.db"
import pytest  # noqa: E402
from src import storage  # noqa: E402
storage.init_db()
@pytest.fixture(autouse=True)
def clean_db():
    with storage.get_connection() as conn:
        conn.execute("DELETE FROM links")
        conn.commit()
    yield
