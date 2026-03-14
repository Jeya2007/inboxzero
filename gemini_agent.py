import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are InboxZero, an expert email triage AI assistant.
For each email, you must respond ONLY with valid JSON in this exact format:
{
  "category": "ACTION_REQUIRED | MEETING_REQUEST | FYI | SPAM | URGENT",
  "priority": "HIGH | MEDIUM | LOW",
  "summary": "One sentence summary of the email",
  "suggested_reply": "A professional reply draft or null if no reply needed",
  "action": "REPLY | CREATE_CALENDAR_EVENT | FLAG_URGENT | ARCHIVE | null",
  "meeting_details": {
    "title": "Meeting title if action is CREATE_CALENDAR_EVENT else null",
    "proposed_time": "Proposed time if mentioned else null"
  }
}
Do not include any text outside the JSON object."""

def analyze_email(email: dict) -> dict:
    prompt = f"""{SYSTEM_PROMPT}

Analyze this email:

From: {email['sender']}
Subject: {email['subject']}
Date: {email['date']}

Body:
{email['body']}
"""
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        result_text = result_text.replace('```json', '').replace('```', '').strip()
        return json.loads(result_text)
    except Exception as e:
        return {
            "category": "FYI",
            "priority": "LOW",
            "summary": f"Analysis failed: {str(e)}",
            "suggested_reply": None,
            "action": None,
            "meeting_details": {"title": None, "proposed_time": None}
        }

def refine_reply(original_email: dict, draft: str, instruction: str) -> str:
    prompt = f"""Original email from {original_email['sender']}:
{original_email['body']}

Current draft reply:
{draft}

User instruction: {instruction}

Rewrite the reply based on the instruction. Return ONLY the refined email body text."""
    response = model.generate_content(prompt)
    return response.text.strip()