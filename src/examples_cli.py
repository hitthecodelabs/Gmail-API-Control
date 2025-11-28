import os
from src.gmail_auth import load_credentials_from_env
from src.gmail_actions import build_gmail_service, list_messages, get_message

def main():
    creds, refreshed = load_credentials_from_env()

    # Si refrescó, lo imprimimos para que lo puedas actualizar en Railway si quieres
    if refreshed:
        print("🔄 Token refrescado. (Opcional) Actualiza tu ENV con este nuevo JSON:")
        print(refreshed)

    service = build_gmail_service(creds)

    msgs = list_messages(service, max_results=5)
    for m in msgs:
        msg = get_message(service, m["id"])
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(sin asunto)")
        print(m["id"], "=>", subject)

if __name__ == "__main__":
    main()
