"""
Emotion-Aligned Training Model - Experiment 3
Maps emotional state to ideal workout intensity & coaching tone.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import json
import google.generativeai as genai
from shared.config import config

app = FastAPI(
    title="Emotion-Aligned Training Model",
    description="Maps emotional state to ideal workout intensity & coaching tone",
    version="1.0.0"
)

# Set up templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Load emotion mapping data
emotion_data_path = Path(__file__).parent.parent.parent / "datasets" / "emotion-mapping.json"
with open(emotion_data_path, 'r') as f:
    emotion_mapping = json.load(f)


class EmotionInput(BaseModel):
    """Input schema for emotion-based workout generation."""
    
    mood: str = Field(..., description="Current emotional state/mood")
    energy: int = Field(..., ge=1, le=10, description="Current energy level (1-10)")
    stress: int = Field(..., ge=1, le=10, description="Current stress level (1-10)")
    
    @validator('mood')
    def validate_mood(cls, v):
        valid_moods = ['anxious', 'energetic', 'tired', 'motivated', 'frustrated', 
                       'sad', 'overwhelmed', 'confident', 'restless', 'content', 
                       'excited', 'neutral']
        if v.lower() not in valid_moods:
            raise ValueError(f'mood must be one of: {", ".join(valid_moods)}')
        return v.lower()


class EmotionRecommendation(BaseModel):
    """Output schema for emotion-based recommendations."""
    
    mood: str
    energy: int
    stress: int
    recommended_session: str
    coaching_style: str
    reason: str
    workout_types: List[str]
    duration_range: List[int]
    intensity: str
    coaching_details: Dict[str, Any]
    example_phrases: List[str]


def get_emotion_recommendation(mood: str, energy: int, stress: int) -> Dict[str, Any]:
    """
    Get workout recommendation based on emotional state.
    
    Args:
        mood: User's current mood
        energy: Energy level (1-10)
        stress: Stress level (1-10)
        
    Returns:
        Dictionary with workout recommendations
    """
    
    # Find matching mood mapping
    mood_mapping = None
    for mapping in emotion_mapping['mappings']:
        if mapping['mood'] == mood:
            mood_mapping = mapping
            break
    
    if not mood_mapping:
        raise HTTPException(status_code=400, detail=f"Mood '{mood}' not found in mapping data")
    
    # Get coaching tone details
    coaching_tone = mood_mapping['coaching_tone']
    coaching_details = emotion_mapping['coaching_tones'].get(coaching_tone, {})
    
    # Get intensity details
    intensity = mood_mapping['recommended_intensity']
    intensity_details = emotion_mapping['intensity_guidelines'].get(intensity, {})
    
    # Select example session
    example_sessions = mood_mapping.get('example_sessions', [])
    recommended_session = example_sessions[0] if example_sessions else "Custom session"
    
    return {
        'mood': mood,
        'energy': energy,
        'stress': stress,
        'recommended_session': recommended_session,
        'coaching_style': coaching_tone,
        'reason': mood_mapping['why_this_works'],
        'workout_types': mood_mapping['workout_types'],
        'duration_range': mood_mapping['duration'],
        'intensity': intensity,
        'intensity_details': intensity_details,
        'coaching_details': coaching_details,
        'example_phrases': coaching_details.get('example_phrases', []),
        'all_example_sessions': example_sessions
    }


async def generate_ai_session(recommendation: Dict[str, Any]) -> str:
    """
    Use Gemini to generate a personalized session description.
    
    Args:
        recommendation: Base recommendation data
        
    Returns:
        AI-generated session description
    """
    
    config.validate()
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    prompt = f"""You are an empathetic fitness coach creating a personalized workout session.

User's Emotional State:
- Mood: {recommendation['mood']}
- Energy Level: {recommendation['energy']}/10
- Stress Level: {recommendation['stress']}/10

Recommended Parameters:
- Intensity: {recommendation['intensity']}
- Coaching Tone: {recommendation['coaching_style']}
- Duration: {recommendation['duration_range'][0]}-{recommendation['duration_range'][1]} minutes
- Workout Types: {', '.join(recommendation['workout_types'])}

Generate a warm, personalized 2-3 sentence session introduction that:
1. Acknowledges their emotional state
2. Explains why this session will help
3. Uses the {recommendation['coaching_style']} coaching tone
4. Feels authentic and supportive

Keep it concise and conversational. No generic fitness clichés."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Fallback to template-based message
        return f"Given how you're feeling {recommendation['mood']} today, this {recommendation['intensity']} intensity session is designed to meet you where you are. {recommendation['reason']}"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with emotion input form."""
    
    # Get list of valid moods for the form
    valid_moods = [mapping['mood'] for mapping in emotion_mapping['mappings']]
    
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "valid_moods": valid_moods
        }
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_recommendation(request: Request, emotion_input: EmotionInput):
    """Generate emotion-aligned workout recommendation."""
    
    # Get base recommendation
    recommendation = get_emotion_recommendation(
        mood=emotion_input.mood,
        energy=emotion_input.energy,
        stress=emotion_input.stress
    )
    
    # Generate AI personalization
    ai_message = await generate_ai_session(recommendation)
    recommendation['ai_message'] = ai_message
    
    return templates.TemplateResponse(
        "emotion_card.html",
        {
            "request": request,
            "data": recommendation
        }
    )


@app.get("/demo", response_class=HTMLResponse)
async def demo(request: Request):
    """Demo endpoint with pre-filled anxious example."""
    
    # Demo with anxious mood
    recommendation = get_emotion_recommendation(
        mood="anxious",
        energy=3,
        stress=7
    )
    
    # Generate AI personalization
    ai_message = await generate_ai_session(recommendation)
    recommendation['ai_message'] = ai_message
    
    return templates.TemplateResponse(
        "emotion_card.html",
        {
            "request": request,
            "data": recommendation
        }
    )


@app.get("/api/recommendation")
async def api_recommendation(mood: str, energy: int, stress: int):
    """API endpoint returning JSON recommendation."""
    
    # Validate inputs
    emotion_input = EmotionInput(mood=mood, energy=energy, stress=stress)
    
    # Get recommendation
    recommendation = get_emotion_recommendation(
        mood=emotion_input.mood,
        energy=emotion_input.energy,
        stress=emotion_input.stress
    )
    
    # Generate AI message
    ai_message = await generate_ai_session(recommendation)
    recommendation['ai_message'] = ai_message
    
    return recommendation


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
