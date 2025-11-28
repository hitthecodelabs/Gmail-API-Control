import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build

def build_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)

def list_messages(service, query=None, max_results=10):
    res = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    return res.get("messages", [])

def get_message(service, msg_id, fmt="full"):
    return service.users().messages().get(userId="me", id=msg_id, format=fmt).execute()

def _encode_mime(mime_msg):
    raw = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode("utf-8")
    return {"raw": raw}

def send_plain_email(service, sender, to, subject, body_text):
    msg = MIMEText(body_text, "plain", "utf-8")
    msg["To"] = to
    msg["From"] = sender
    msg["Subject"] = subject
    return service.users().messages().send(userId="me", body=_encode_mime(msg)).execute()
