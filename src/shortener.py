"""Generation de codes courts uniques pour les liens raccourcis."""

import secrets
import string

from src.storage import code_exists

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_ATTEMPTS = 10


def generate_unique_code() -> str:
    """Genere un code alphanumerique de 6 caracteres garanti unique en base.

    Reessaie jusqu'a MAX_ATTEMPTS fois en cas de collision (tres rare avec
    62^6 combinaisons possibles) avant d'abandonner explicitement.
    """
    for _ in range(MAX_ATTEMPTS):
        candidate = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if not code_exists(candidate):
            return candidate

    raise RuntimeError(
        f"Impossible de generer un code court unique apres {MAX_ATTEMPTS} tentatives."
    )
