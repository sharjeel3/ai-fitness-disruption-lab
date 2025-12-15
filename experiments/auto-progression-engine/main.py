"""
Auto-Progression Engine (APE) - Experiment 2
AI-powered workout progression tracking and recommendations.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, validator
import json
from shared.gemini_client import gemini_client
from shared.config import config

app = FastAPI(
    title="Auto-Progression Engine (APE)",
    description="AI-powered workout progression tracking and recommendations",
    version="1.0.0"
)

# Set up templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


class WorkoutEntry(BaseModel):
    """Single workout entry."""
    
    exercise: str = Field(..., description="Exercise name")
    weight: float = Field(..., ge=0, description="Weight used (kg)")
    sets: int = Field(..., ge=1, le=10, description="Number of sets")
    reps: int = Field(..., ge=1, le=50, description="Number of reps")
    rpe: int = Field(..., ge=1, le=10, description="Rate of Perceived Exertion (1-10)")
    date: Optional[str] = Field(default=None, description="Date of workout (YYYY-MM-DD)")
    notes: Optional[str] = Field(default=None, description="Additional notes")
    
    @validator('date', pre=True, always=True)
    def set_default_date(cls, v):
        if v is None:
            return datetime.now().strftime("%Y-%m-%d")
        return v


class ProgressionInput(BaseModel):
    """Input schema for progression analysis."""
    
    exercise: str = Field(..., description="Exercise to analyze")
    history: List[WorkoutEntry] = Field(..., min_items=2, description="Workout history (minimum 2 entries)")
    goal: str = Field(default="strength", description="Training goal: strength, hypertrophy, or endurance")
    
    @validator('goal')
    def validate_goal(cls, v):
        allowed = ['strength', 'hypertrophy', 'endurance']
        if v.lower() not in allowed:
            raise ValueError(f'goal must be one of: {", ".join(allowed)}')
        return v.lower()


class ProgressionRecommendation(BaseModel):
    """Progression recommendation output."""
    
    exercise: str
    current_performance: Dict[str, Any]
    recommended_next: Dict[str, Any]
    progression_rate: str
    rationale: str
    deload_suggested: bool
    tips: List[str]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with workout logging form."""
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/demo", response_class=HTMLResponse)
async def demo(request: Request):
    """Demo endpoint with pre-filled progression example."""
    
    # Demo workout history
    demo_data = ProgressionInput(
        exercise="Barbell Squat",
        history=[
            WorkoutEntry(exercise="Barbell Squat", weight=60, sets=3, reps=10, rpe=7, 
                        date="2024-12-01", notes="Felt strong"),
            WorkoutEntry(exercise="Barbell Squat", weight=62.5, sets=3, reps=10, rpe=7, 
                        date="2024-12-04", notes="Good form"),
            WorkoutEntry(exercise="Barbell Squat", weight=65, sets=3, reps=9, rpe=8, 
                        date="2024-12-07", notes="Slight struggle on last set"),
            WorkoutEntry(exercise="Barbell Squat", weight=65, sets=3, reps=10, rpe=7, 
                        date="2024-12-11", notes="Better than last time"),
            WorkoutEntry(exercise="Barbell Squat", weight=67.5, sets=3, reps=10, rpe=8, 
                        date="2024-12-14", notes="Ready for more"),
        ],
        goal="strength"
    )
    
    # Generate progression recommendation
    recommendation = await analyze_progression(demo_data)
    
    # Prepare chart data
    chart_data = prepare_chart_data(demo_data.history)
    
    return templates.TemplateResponse(
        "progression_dashboard.html",
        {
            "request": request,
            "exercise": demo_data.exercise,
            "goal": demo_data.goal,
            "history": demo_data.history,
            "recommendation": recommendation,
            "chart_data": chart_data
        }
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_progression_endpoint(request: Request, progression_input: ProgressionInput):
    """
    Analyze workout progression and generate recommendations.
    
    Returns a mobile-first HTML view of the progression dashboard.
    """
    
    try:
        # Generate progression recommendation
        recommendation = await analyze_progression(progression_input)
        
        # Prepare chart data
        chart_data = prepare_chart_data(progression_input.history)
        
        # Return rendered HTML template
        return templates.TemplateResponse(
            "progression_dashboard.html",
            {
                "request": request,
                "exercise": progression_input.exercise,
                "goal": progression_input.goal,
                "history": progression_input.history,
                "recommendation": recommendation,
                "chart_data": chart_data
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-json")
async def analyze_progression_json(progression_input: ProgressionInput):
    """
    Analyze workout progression and return as JSON.
    
    Useful for API integrations and testing.
    """
    
    try:
        recommendation = await analyze_progression(progression_input)
        
        return {
            "status": "success",
            "input": progression_input.dict(),
            "recommendation": recommendation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "experiment": "Auto-Progression Engine (APE)",
        "version": "1.0.0"
    }


async def analyze_progression(progression_input: ProgressionInput) -> Dict[str, Any]:
    """
    Analyze workout history and generate progression recommendations using Gemini.
    
    Args:
        progression_input: Workout history and analysis parameters
        
    Returns:
        Dictionary containing progression recommendations
    """
    
    # Prepare history summary for Gemini
    history_summary = "\n".join([
        f"- {entry.date}: {entry.sets}x{entry.reps} @ {entry.weight}kg, RPE {entry.rpe}"
        for entry in progression_input.history
    ])
    
    # Calculate basic stats
    latest = progression_input.history[-1]
    earliest = progression_input.history[0]
    weight_increase = latest.weight - earliest.weight
    avg_rpe = sum(entry.rpe for entry in progression_input.history) / len(progression_input.history)
    
    prompt = f"""You are an expert strength coach analyzing workout progression data.

EXERCISE: {progression_input.exercise}
TRAINING GOAL: {progression_input.goal}

WORKOUT HISTORY:
{history_summary}

CURRENT STATS:
- Latest workout: {latest.sets}x{latest.reps} @ {latest.weight}kg, RPE {latest.rpe}
- Total weight increase: {weight_increase}kg over {len(progression_input.history)} sessions
- Average RPE: {avg_rpe:.1f}/10

INSTRUCTIONS:
1. Analyze the progression pattern (is the athlete improving consistently?)
2. Evaluate RPE trends (are they managing fatigue well?)
3. Recommend the next workout prescription based on their goal:
   - Strength: Focus on progressive overload (weight or reps)
   - Hypertrophy: Focus on volume and time under tension
   - Endurance: Focus on reps and work capacity
4. Determine if a deload is needed (if RPE consistently high or performance stalling)
5. Provide 2-3 specific coaching tips

SAFETY RULES:
- Never recommend more than 5% weight increase per session
- If last RPE was 9-10, recommend same weight or deload
- If performance declined, recommend maintaining or reducing load
- Always prioritize sustainable progression over aggressive gains

Return your response in this JSON format:
{{
  "exercise": "{progression_input.exercise}",
  "current_performance": {{
    "weight": {latest.weight},
    "sets": {latest.sets},
    "reps": {latest.reps},
    "rpe": {latest.rpe},
    "volume": (calculate sets * reps * weight)
  }},
  "recommended_next": {{
    "weight": (recommended weight in kg),
    "sets": (recommended sets),
    "reps": (recommended reps),
    "target_rpe": (target RPE 1-10)
  }},
  "progression_rate": "conservative/moderate/aggressive",
  "rationale": "Brief explanation of why this progression is appropriate",
  "deload_suggested": true/false,
  "tips": [
    "Specific coaching tip 1",
    "Specific coaching tip 2",
    "Specific coaching tip 3"
  ]
}}
"""
    
    try:
        response = await gemini_client.generate_text(prompt)
        
        # Extract JSON from response
        response_text = response.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        recommendation = json.loads(response_text.strip())
        return recommendation
        
    except json.JSONDecodeError as e:
        # Fallback response if JSON parsing fails
        next_weight = latest.weight + 2.5 if latest.rpe < 8 else latest.weight
        return {
            "exercise": progression_input.exercise,
            "current_performance": {
                "weight": latest.weight,
                "sets": latest.sets,
                "reps": latest.reps,
                "rpe": latest.rpe,
                "volume": latest.sets * latest.reps * latest.weight
            },
            "recommended_next": {
                "weight": next_weight,
                "sets": latest.sets,
                "reps": latest.reps,
                "target_rpe": 7
            },
            "progression_rate": "moderate",
            "rationale": f"Conservative progression based on recent performance (parsing error: {str(e)})",
            "deload_suggested": False,
            "tips": [
                "Focus on maintaining good form",
                "Monitor RPE carefully",
                "Progressive overload should be gradual"
            ]
        }
    except Exception as e:
        raise Exception(f"Error analyzing progression: {str(e)}")


def prepare_chart_data(history: List[WorkoutEntry]) -> Dict[str, List]:
    """
    Prepare data for charts in the dashboard.
    
    Args:
        history: List of workout entries
        
    Returns:
        Dictionary with chart data arrays
    """
    
    dates = [entry.date for entry in history]
    weights = [entry.weight for entry in history]
    rpes = [entry.rpe for entry in history]
    volumes = [entry.sets * entry.reps * entry.weight for entry in history]
    
    return {
        "dates": dates,
        "weights": weights,
        "rpes": rpes,
        "volumes": volumes
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
