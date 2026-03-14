def fetch_unread_emails(max_results=10):
    return [
        {
            'id': '1',
            'subject': 'Urgent: Project deadline moved to tomorrow',
            'sender': 'manager@company.com',
            'date': 'Sat, 14 Mar 2026 09:00:00',
            'body': 'Hi, I wanted to let you know that the project deadline has been moved to tomorrow at 5 PM. Please make sure all deliverables are ready. This is critical for our client presentation. Let me know if you have any blockers.'
        },
        {
            'id': '2',
            'subject': 'Meeting request: Product sync next week',
            'sender': 'teammate@company.com',
            'date': 'Sat, 14 Mar 2026 08:30:00',
            'body': 'Hey, can we schedule a product sync meeting next Tuesday at 2 PM? I want to discuss the new feature roadmap and get everyone aligned before the sprint starts. Please confirm if that works for you.'
        },
        {
            'id': '3',
            'subject': 'Invoice #1042 payment confirmation',
            'sender': 'billing@vendor.com',
            'date': 'Sat, 14 Mar 2026 07:15:00',
            'body': 'Dear Customer, your payment of $1,200 for Invoice #1042 has been successfully processed. Your subscription is now active until March 2027. Thank you for your business.'
        },
        {
            'id': '4',
            'subject': 'You won a FREE iPhone 15 Pro!!!',
            'sender': 'noreply@spam-offers.com',
            'date': 'Sat, 14 Mar 2026 06:00:00',
            'body': 'Congratulations! You have been selected as our lucky winner. Click here now to claim your FREE iPhone 15 Pro. Limited time offer. Act now!!!'
        },
        {
            'id': '5',
            'subject': 'Code review needed: Auth module PR #234',
            'sender': 'developer@company.com',
            'date': 'Fri, 13 Mar 2026 18:00:00',
            'body': 'Hi, I have submitted PR #234 for the authentication module refactor. Could you review it when you get a chance? There are some important security improvements that need a second pair of eyes before we merge to main.'
        },
        {
            'id': '6',
            'subject': 'Q1 Performance Review scheduled',
            'sender': 'hr@company.com',
            'date': 'Fri, 13 Mar 2026 17:00:00',
            'body': 'Dear Employee, your Q1 performance review has been scheduled for March 20th at 10 AM with your manager. Please prepare a self-assessment and list of achievements. The meeting will be held in Conference Room B.'
        },
        {
            'id': '7',
            'subject': 'AWS bill for February 2026',
            'sender': 'billing@aws.amazon.com',
            'date': 'Fri, 13 Mar 2026 12:00:00',
            'body': 'Your AWS bill for February 2026 is now available. Total charges: $45.23. Your payment method on file will be charged on March 20th. Log in to your AWS console to view the detailed breakdown.'
        },
        {
            'id': '8',
            'subject': 'Team lunch tomorrow - please confirm',
            'sender': 'colleague@company.com',
            'date': 'Fri, 13 Mar 2026 11:30:00',
            'body': 'Hey team! We are organizing a team lunch tomorrow at 1 PM at The Grand Restaurant. Please reply to confirm your attendance so I can make the reservation. Looking forward to seeing everyone!'
        }
    ]

def send_email(to, subject, body):
    print(f"[MOCK SEND] To: {to} | Subject: {subject}")
    return True

def mark_as_read(email_id):
    print(f"[MOCK] Marked email {email_id} as read")