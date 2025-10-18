from django.shortcuts import render, redirect
#import installed app flow
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from googleapiclient.discovery import build
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from .models import Email, msg
from google_auth_oauthlib.flow import Flow 


CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR,'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = 'http://127.0.0.1:8000/google/callback/'
def home(request):
    return HttpResponse("Welcome! <a href='/google/login/'>Login with Google</a>")

def google_login_view(request):
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    
    authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
    
    request.session['state'] = state
    return redirect(authorization_url)

def google_callback(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_response=request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    service = build('gmail', 'v1', credentials=credentials)
    
    result = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = result.get('messages', [])

    email_data = []
    for message in messages:
        message_detail = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = message_detail['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'subject'),'no subject')
        sender = next((h['value'] for h in headers if h['name']=='from'),'unknown')
        snippet = message_detail.get('snippet','(no snippet)')
        email_data.append({
            'subject': subject,
            'sender': sender,
            'snippet': snippet
        })
        return render(request,'emails.html',{'emails':email_data})


def fetch_emails(request):
    creds=None
    if(os.path.exists('token.json')):
        creds=Credentials.from_authorized_user_file('token.json',SCOPES)
        
    if not creds or not creds.valid:
        return HttpResponse("No valid credentials. Please login first.")
    service=build('gmail','v1',credentials=creds)
    try:
        results = service.users().message().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        email_subjects = []
        if not messages:
            return HttpResponse("No messages found.")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute
            headers = msg.get('snippet','(no snippet)')
        return HttpResponse("<br>".join(email_subjects))
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")            