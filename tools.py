def create_calendar_event(title, proposed_time, attendee_email):
    print(f"[MOCK CALENDAR] Event: {title} | Time: {proposed_time} | Attendee: {attendee_email}")
    return "https://calendar.google.com/mock-event-link"

def flag_urgent(email_id):
    print(f"[MOCK] Email {email_id} flagged as urgent ⭐")
    return "Flagged as urgent ⭐"