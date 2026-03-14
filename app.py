import streamlit as st
from gmail_client import fetch_unread_emails, send_email, mark_as_read
from gemini_agent import analyze_email, refine_reply
from tools import create_calendar_event, flag_urgent

st.set_page_config(page_title="InboxZero Agent", page_icon="📬", layout="wide")

st.markdown("# 📬 InboxZero")
st.markdown("*Your autonomous AI email chief of staff — powered by Amazon Nova & Gemini*")
st.divider()

PRIORITY_COLOR = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
CATEGORY_EMOJI = {
    "URGENT": "🚨", "ACTION_REQUIRED": "⚡",
    "MEETING_REQUEST": "📅", "FYI": "ℹ️", "SPAM": "🗑️"
}

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### ⚙️ Controls")
    max_emails = st.slider("Emails to fetch", 5, 20, 8)
    run = st.button("🚀 Run InboxZero Agent", type="primary", use_container_width=True)
    
    if run:
        with st.spinner("📬 Fetching emails..."):
            emails = fetch_unread_emails(max_emails)
        if not emails:
            st.info("🎉 Inbox is already zero!")
        else:
            analyzed = []
            progress = st.progress(0)
            status = st.empty()
            for i, email in enumerate(emails):
                status.markdown(f"🤖 Analyzing **{i+1}/{len(emails)}**...")
                analysis = analyze_email(email)
                analyzed.append({'email': email, 'analysis': analysis})
                progress.progress((i + 1) / len(emails))
            status.markdown("✅ Done!")
            st.session_state['analyzed'] = analyzed

    if 'analyzed' in st.session_state:
        total = len(st.session_state['analyzed'])
        urgent = sum(1 for x in st.session_state['analyzed'] if x['analysis'].get('priority') == 'HIGH')
        meetings = sum(1 for x in st.session_state['analyzed'] if x['analysis'].get('category') == 'MEETING_REQUEST')
        spam = sum(1 for x in st.session_state['analyzed'] if x['analysis'].get('category') == 'SPAM')
        st.divider()
        st.markdown("### 📊 Summary")
        st.metric("Total Emails", total)
        st.metric("🔴 Urgent", urgent)
        st.metric("📅 Meetings", meetings)
        st.metric("🗑️ Spam", spam)

with col2:
    if 'analyzed' not in st.session_state:
        st.markdown("""
        ### 👋 Welcome to InboxZero!
        
        Click **Run InboxZero Agent** to:
        - 📋 Auto-classify all your emails
        - ✉️ Get AI-drafted replies
        - 📅 Create calendar events
        - ⭐ Flag urgent emails
        - 🗑️ Identify spam instantly
        """)
    else:
        st.markdown(f"### 📧 Analyzed Emails")
        for item in st.session_state['analyzed']:
            email = item['email']
            analysis = item['analysis']
            priority = analysis.get('priority', 'LOW')
            category = analysis.get('category', 'FYI')

            with st.expander(
                f"{PRIORITY_COLOR.get(priority,'⚪')} {CATEGORY_EMOJI.get(category,'📧')} "
                f"**{email['subject'][:55]}** — *{email['sender'][:35]}*"
            ):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**📋 Summary:** {analysis.get('summary', '')}")
                    st.markdown(f"**🏷️ Category:** `{category}`")
                    st.markdown(f"**⚡ Priority:** `{priority}`")
                with col_b:
                    action = analysis.get('action', '')
                    if action == 'FLAG_URGENT':
                        if st.button("⭐ Flag Urgent", key=f"flag_{email['id']}"):
                            flag_urgent(email['id'])
                            st.success("Flagged as urgent!")
                    elif action == 'CREATE_CALENDAR_EVENT':
                        details = analysis.get('meeting_details', {})
                        if st.button("📅 Create Calendar Event", key=f"cal_{email['id']}"):
                            sender_email = email['sender'].split('<')[-1].rstrip('>')
                            create_calendar_event(
                                details.get('title', email['subject']),
                                details.get('proposed_time', ''),
                                sender_email
                            )
                            st.success("📅 Event created!")
                    elif action == 'ARCHIVE':
                        st.info("🗑️ Recommended: Archive this email")

                if analysis.get('suggested_reply'):
                    st.divider()
                    st.markdown("**✉️ AI-Drafted Reply:**")
                    reply_draft = st.text_area(
                        "Edit before sending:",
                        value=analysis['suggested_reply'],
                        key=f"reply_{email['id']}", height=120
                    )
                    refine_col, send_col = st.columns(2)
                    with refine_col:
                        refine_instruction = st.text_input(
                            "✨ Refine (e.g. 'make shorter'):",
                            key=f"refine_{email['id']}"
                        )
                        if refine_instruction and st.button("🔄 Refine with AI", key=f"rfbtn_{email['id']}"):
                            with st.spinner("Refining..."):
                                refined = refine_reply(email, reply_draft, refine_instruction)
                            st.text_area("Refined reply:", value=refined, key=f"refined_{email['id']}")
                    with send_col:
                        st.markdown("<br>", unsafe_allow_html=True)
                        sender_email = email['sender'].split('<')[-1].rstrip('>')
                        if st.button("📤 Send Reply", key=f"send_{email['id']}", type="primary"):
                            send_email(sender_email, f"Re: {email['subject']}", reply_draft)
                            mark_as_read(email['id'])
                            st.success("✅ Reply sent!")