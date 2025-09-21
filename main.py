import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
import json
from agents import Runner,trace
from network_agents.network_manager import network_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

app = FastAPI(title="Network Bot API", version="0.1.0")

# Request/Response models
class OutreachRequest(BaseModel):
    platform: Literal["twitter", "instagram", "linkedin"]
    interaction_stage: Literal[
        "first_contact", "follow_up_1", "follow_up_2", "warm_nudge",
        "post_meeting_thanks", "ask_for_intro", "close_breakup",
        "social_reply", "social_comment"
    ]
    tone: Literal["casual", "professional", "busy"]
    person_name: Optional[str] = None
    why: Optional[str] = None
    context: Optional[str] = None

class OutreachResponse(BaseModel):
    platform: str
    interaction_stage: str
    tone: str
    person_name: Optional[str] = None
    why: Optional[str] = None
    subject: Optional[str] = None
    message: str
    context: Optional[str] = None
    length_chars: int
    personalization_clues: list = []
    next_steps: list = []
    safety_checks_passed: bool = True
    reasons_for_denial: Optional[list] = None

@app.get("/")
async def root():
    return {"message": "Network Bot API is running"}

@app.post("/outreach", response_model=OutreachResponse)
async def generate_outreach(request: OutreachRequest):
    """
    Generate platform-specific outreach messages using the network manager agent.
    """
    logger.info(f"Received outreach request: {request}")
    
    try:
        # Convert request to JSON string for the agent
        query_dict = request.model_dump()
        query_str = json.dumps(query_dict, ensure_ascii=False)
        logger.info(f"Query string: {query_str}")
        
        # Check if network_manager is properly loaded
        logger.info(f"Network manager type: {type(network_manager)}")
        logger.info(f"Network manager: {network_manager}")
        
        # Run the network manager agent
        logger.info("Starting agent execution...")
        result = await Runner.run(network_manager, query_str)
        logger.info(f"Agent execution completed. Result type: {type(result)}")
        logger.info(f"Result: {result}")
        
        # Extract the response from the agent
        if hasattr(result, 'final_output') and result.final_output:
            response_data = result.final_output
            logger.info(f"Final output type: {type(response_data)}")
            logger.info(f"Final output: {response_data}")
            
            # Parse JSON string if needed
            if isinstance(response_data, str):
                try:
                    # Remove markdown code blocks if present
                    if response_data.strip().startswith('```json'):
                        # Extract JSON from markdown code block
                        lines = response_data.strip().split('\n')
                        json_lines = []
                        in_json = False
                        for line in lines:
                            if line.strip() == '```json':
                                in_json = True
                                continue
                            elif line.strip() == '```':
                                break
                            elif in_json:
                                json_lines.append(line)
                        response_data = '\n'.join(json_lines)
                        logger.info(f"Extracted JSON from markdown: {response_data}")
                    
                    response_data = json.loads(response_data)
                    logger.info(f"Parsed JSON: {response_data}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {e}")
                    logger.error(f"Raw response: {repr(response_data)}")
                    raise HTTPException(status_code=500, detail=f"Invalid JSON response from agent: {e}")
        else:
            logger.error("Agent did not return valid output")
            logger.error(f"Result attributes: {dir(result)}")
            raise HTTPException(status_code=500, detail="Agent did not return valid output")
        
        # Convert to response model
        logger.info("Converting to response model...")
        response = OutreachResponse(**response_data)
        logger.info(f"Response created successfully: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error in generate_outreach: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating outreach: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test-agent")
async def test_agent():
    """Test endpoint to verify the network manager is working"""
    try:
        logger.info("Testing network manager...")
        logger.info(f"Network manager: {network_manager}")
        logger.info(f"Network manager type: {type(network_manager)}")
        return {
            "status": "success",
            "network_manager_type": str(type(network_manager)),
            "network_manager_name": getattr(network_manager, 'name', 'Unknown')
        }
    except Exception as e:
        logger.error(f"Error testing agent: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
