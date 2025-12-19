"""
Fitness Persona Generator Prototype
Generates unique fitness identity cards based on user traits, goals, and preferences.
"""

import json
import sys
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import google.generativeai as genai

# Add shared directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from shared.config import config

# Initialize FastAPI app
app = FastAPI(
    title="Fitness Persona Generator",
    description="Generate unique fitness identity cards using AI",
    version="1.0.0"
)

# Set up templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Initialize Gemini
config.validate()
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel(config.GEMINI_MODEL)

# Load persona archetypes
personas_file = Path(__file__).parent.parent.parent / "datasets" / "personas.json"
with open(personas_file, "r") as f:
    personas_data = json.load(f)


# Request Models
class PersonaInput(BaseModel):
    """Input model for persona generation."""
    traits: List[str] = Field(
        ..., 
        description="User personality traits (e.g., disciplined, creative, spontaneous)",
        min_items=1,
        max_items=5
    )
    goals: List[str] = Field(
        ...,
        description="Fitness goals (e.g., lean, strength, flexibility, endurance)",
        min_items=1,
        max_items=3
    )
    music_preference: str = Field(
        ...,
        description="Preferred workout music genre (e.g., pop, rock, instrumental, ambient)"
    )
    workout_style: Optional[str] = Field(
        None,
        description="Preferred workout style (e.g., intense, gentle, varied)"
    )
    session_length_preference: Optional[int] = Field(
        None,
        description="Preferred session length in minutes",
        ge=10,
        le=120
    )


class PersonaOutput(BaseModel):
    """Output model for generated persona."""
    persona_name: str
    archetype_match: Optional[str] = None
    style: str
    tagline: str
    traits: List[str]
    goals: List[str]
    color_palette: List[str]
    music_preference: str
    workout_approach: str
    ideal_session_length: int
    recovery_priority: str
    description: str
    motivation_quote: str


async def generate_persona(input_data: PersonaInput) -> PersonaOutput:
    """
    Generate a unique fitness persona using Gemini LLM.
    
    Args:
        input_data: User input containing traits, goals, and preferences
        
    Returns:
        PersonaOutput with generated persona details
    """
    
    # Create context from existing archetypes
    archetypes_context = json.dumps(personas_data["archetypes"], indent=2)
    
    prompt = f"""You are an expert fitness persona designer. Create a unique, inspiring fitness identity for a user.

EXISTING ARCHETYPES (for reference and inspiration):
{archetypes_context}

USER INPUT:
- Traits: {', '.join(input_data.traits)}
- Goals: {', '.join(input_data.goals)}
- Music Preference: {input_data.music_preference}
- Workout Style: {input_data.workout_style or 'Not specified'}
- Session Length Preference: {input_data.session_length_preference or 'Not specified'}

TASK:
1. Analyze the user's traits and goals
2. Find the best matching archetype OR create a unique hybrid persona
3. Generate a creative, empowering persona name (format: "The [Adjective] [Noun]")
4. Create a memorable 3-word tagline (format: "Verb. Verb. Verb.")
5. Choose a color palette (2 hex codes that match the persona's energy)
6. Define workout approach and recovery priority
7. Write a 2-3 sentence inspiring description
8. Create a motivational quote that embodies this persona

GUIDELINES:
- Persona names should be inspiring and memorable
- Taglines must be action-oriented and rhythmic
- Color palettes should reflect the persona's energy (bold for intense, calm for gentle)
- Keep descriptions concise but powerful
- Ensure the persona feels authentic and aspirational

Return ONLY valid JSON with this exact structure:
{{
  "persona_name": "The [Adjective] [Noun]",
  "archetype_match": "name of closest archetype or null if unique",
  "style": "description of training style",
  "tagline": "Verb. Verb. Verb.",
  "traits": ["trait1", "trait2", "trait3"],
  "goals": ["goal1", "goal2"],
  "color_palette": ["#HEX1", "#HEX2"],
  "music_preference": "{input_data.music_preference}",
  "workout_approach": "approach_description",
  "ideal_session_length": 45,
  "recovery_priority": "low/medium/high",
  "description": "2-3 sentence inspiring description of this persona",
  "motivation_quote": "A powerful quote that embodies this persona's spirit"
}}"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON response
        persona_data = json.loads(response_text)
        
        return PersonaOutput(**persona_data)
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating persona: {str(e)}"
        )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with input form."""
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "archetypes": personas_data["archetypes"]
        }
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_persona_endpoint(
    request: Request,
    traits: str = Form(...),
    goals: str = Form(...),
    music_preference: str = Form(...),
    workout_style: Optional[str] = Form(None),
    session_length_preference: Optional[str] = Form(None)
):
    """Generate and display a fitness persona."""
    
    # Parse JSON strings from form
    try:
        traits_list = json.loads(traits)
        goals_list = json.loads(goals)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid traits or goals format"
        )
    
    # Parse session length if provided
    session_length = None
    if session_length_preference and session_length_preference.strip():
        try:
            session_length = int(session_length_preference)
        except ValueError:
            pass
    
    # Create PersonaInput
    input_data = PersonaInput(
        traits=traits_list,
        goals=goals_list,
        music_preference=music_preference,
        workout_style=workout_style if workout_style and workout_style.strip() else None,
        session_length_preference=session_length
    )
    
    # Generate persona using Gemini
    persona = await generate_persona(input_data)
    
    # Save to outputs (optional)
    output_file = Path(__file__).parent / "outputs" / "latest_persona.json"
    with open(output_file, "w") as f:
        json.dump(persona.dict(), f, indent=2)
    
    # Render persona card
    return templates.TemplateResponse(
        "persona_card.html",
        {
            "request": request,
            "persona": persona
        }
    )


@app.get("/demo", response_class=HTMLResponse)
async def demo(request: Request):
    """Demo endpoint with pre-filled data."""
    
    # Example input
    demo_input = PersonaInput(
        traits=["disciplined", "creative", "consistent"],
        goals=["strength", "lean"],
        music_preference="instrumental",
        workout_style="controlled intensity",
        session_length_preference=45
    )
    
    # Generate persona
    persona = await generate_persona(demo_input)
    
    # Render persona card
    return templates.TemplateResponse(
        "persona_card.html",
        {
            "request": request,
            "persona": persona
        }
    )


@app.get("/api/archetypes")
async def get_archetypes():
    """Get all persona archetypes."""
    return {"archetypes": personas_data["archetypes"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
