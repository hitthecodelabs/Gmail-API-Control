import os
import json
import base64
from typing import List, Optional, Tuple

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]


def _get_scopes_from_env() -> List[str]:
    raw = os.getenv("GMAIL_SCOPES", "")
    if raw.strip():
        return [s.strip() for s in raw.split(",") if s.strip()]
    return DEFAULT_SCOPES


def load_credentials_from_env() -> Tuple[Credentials, Optional[str]]:
    """
    Retorna:
      - creds: Credentials listo para build()
      - refreshed_token_json: str con JSON actualizado si hubo refresh; si no, None

    Nota: en producción (Railway variables), tú decides si actualizas la variable con refreshed_token_json.
    """
    scopes = _get_scopes_from_env()

    token_b64 = os.getenv("GOOGLE_TOKEN_JSON_B64")
    token_json = os.getenv("GOOGLE_TOKEN_JSON")

    if token_b64:
        try:
            token_json = base64.b64decode(token_b64).decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"GOOGLE_TOKEN_JSON_B64 inválido: {e}")

    if not token_json:
        raise RuntimeError(
            "No hay token en ENV. Define GOOGLE_TOKEN_JSON_B64 (recomendado) o GOOGLE_TOKEN_JSON."
        )

    try:
        token_info = json.loads(token_json)
    except json.JSONDecodeError:
        raise RuntimeError("GOOGLE_TOKEN_JSON no es JSON válido.")

    creds = Credentials.from_authorized_user_info(token_info, scopes=scopes)

    refreshed_token_json = None
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            refreshed_token_json = creds.to_json()
        except RefreshError as e:
            raise RuntimeError(
                f"RefreshError renovando credenciales: {e}. "
                f"Solución: regenera token localmente y actualiza la variable en producción."
            )

    if not creds or not creds.valid:
        raise RuntimeError("Credenciales inválidas. Reautentica y genera un token nuevo.")

    return creds, refreshed_token_json
