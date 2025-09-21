from models.models import OutreachResponse
from agents import Agent


LINKEDIN_INSTRUCTIONS = """
You are a professional LinkedIn outreach writer.
- Produce subject (if requested) and a short message body suitable for LinkedIn/InMail or email.
- Keep message concise (50-200 words for LinkedIn DM).
- Maintain the requested tone and include one CTA (e.g., 10-minute chat).
- If stage is a follow-up, briefly reference previous touchpoint.
Return JSON matching the OutreachResponse schema.
"""

linkedin_agent =  Agent(
        name="LinkedinAgent",
        instructions=LINKEDIN_INSTRUCTIONS,
        model="gpt-4o-mini",
        output_type=OutreachResponse
)