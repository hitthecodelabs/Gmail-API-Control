import argparse
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--credentials", required=True, help="Ruta al credentials.json (OAuth Desktop)")
    p.add_argument("--out", default="token.json", help="Archivo de salida del token (ej: token_s.json)")
    p.add_argument("--scopes", default=",".join(DEFAULT_SCOPES), help="Scopes separados por coma")
    return p.parse_args()


def main():
    args = parse_args()
    scopes = [s.strip() for s in args.scopes.split(",") if s.strip()]

    creds = None
    if os.path.exists(args.out):
        creds = Credentials.from_authorized_user_file(args.out, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(args.credentials, scopes)
            creds = flow.run_local_server(port=0)

        with open(args.out, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    print(f"✅ Token generado/actualizado: {args.out}")


if __name__ == "__main__":
    main()
