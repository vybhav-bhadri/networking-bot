from models.models import OutreachResponse
from agents import Agent


INSTAGRAM_INSTRUCTIONS = """
You are a friendly Instagram comment writer.
- Output a short comment (<= 200 chars recommended).
- Use a compliment or concise insight + 1 short question if appropriate.
- Keep tone aligned to the requested tone.
- Do NOT include personal contact info.
Return JSON matching the OutreachResponse schema.
"""

instagram_agent =  Agent(
        name="InstagramAgent",
        instructions=INSTAGRAM_INSTRUCTIONS,
        model="gpt-4o-mini",
        output_type=OutreachResponse
)