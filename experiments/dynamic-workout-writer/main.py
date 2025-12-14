"""
Dynamic Workout Writer (DW²) - Experiment 1
AI-generated adaptive workouts based on daily conditions.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import json
from shared.gemini_client import gemini_client
from shared.config import config

app = FastAPI(
    title="Dynamic Workout Writer (DW²)",
    description="AI-generated adaptive workouts based on daily conditions",
    version="1.0.0"
)

# Set up templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


class WorkoutInput(BaseModel):
    """Input schema for workout generation."""
    
    fitness_level: str = Field(..., description="Fitness level: beginner, intermediate, or advanced")
    goals: List[str] = Field(..., description="Fitness goals: strength, cardio, flexibility, etc.")
    time_available: int = Field(..., ge=5, le=120, description="Available time in minutes")
    equipment: List[str] = Field(default=["bodyweight"], description="Available equipment")
    fatigue: int = Field(..., ge=1, le=10, description="Current fatigue level (1-10)")
    stress: int = Field(..., ge=1, le=10, description="Current stress level (1-10)")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep last night")
    
    @validator('fitness_level')
    def validate_fitness_level(cls, v):
        allowed = ['beginner', 'intermediate', 'advanced']
        if v.lower() not in allowed:
            raise ValueError(f'fitness_level must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @validator('goals')
    def validate_goals(cls, v):
        if not v:
            raise ValueError('At least one goal must be specified')
        allowed = ['strength', 'cardio', 'flexibility', 'mobility', 'endurance', 'power']
        for goal in v:
            if goal.lower() not in allowed:
                raise ValueError(f'Invalid goal: {goal}. Allowed: {", ".join(allowed)}')
        return [g.lower() for g in v]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with workout generation form."""
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/demo", response_class=HTMLResponse)
async def demo(request: Request):
    """Demo endpoint with pre-filled workout example."""
    
    # Demo workout data
    demo_input = WorkoutInput(
        fitness_level="intermediate",
        goals=["strength"],
        time_available=30,
        equipment=["dumbbells"],
        fatigue=3,
        stress=2,
        sleep_hours=6
    )
    
    # Generate workout
    workout_data = await gemini_client.generate_workout(
        fitness_level=demo_input.fitness_level,
        goals=demo_input.goals,
        time_available=demo_input.time_available,
        equipment=demo_input.equipment,
        fatigue=demo_input.fatigue,
        stress=demo_input.stress,
        sleep_hours=demo_input.sleep_hours
    )
    
    return templates.TemplateResponse(
        "workout_card.html",
        {
            "request": request,
            "workout_data": workout_data,
            "user_input": demo_input.dict()
        }
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_workout(request: Request, workout_input: WorkoutInput):
    """
    Generate an adaptive workout based on user inputs.
    
    Returns a mobile-first HTML view of the workout.
    """
    
    try:
        # Generate workout using Gemini
        workout_data = await gemini_client.generate_workout(
            fitness_level=workout_input.fitness_level,
            goals=workout_input.goals,
            time_available=workout_input.time_available,
            equipment=workout_input.equipment,
            fatigue=workout_input.fatigue,
            stress=workout_input.stress,
            sleep_hours=workout_input.sleep_hours
        )
        
        # Return rendered HTML template
        return templates.TemplateResponse(
            "workout_card.html",
            {
                "request": request,
                "workout_data": workout_data,
                "user_input": workout_input.dict()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-json")
async def generate_workout_json(workout_input: WorkoutInput):
    """
    Generate an adaptive workout and return as JSON.
    
    Useful for API integrations and testing.
    """
    
    try:
        workout_data = await gemini_client.generate_workout(
            fitness_level=workout_input.fitness_level,
            goals=workout_input.goals,
            time_available=workout_input.time_available,
            equipment=workout_input.equipment,
            fatigue=workout_input.fatigue,
            stress=workout_input.stress,
            sleep_hours=workout_input.sleep_hours
        )
        
        return {
            "status": "success",
            "input": workout_input.dict(),
            "output": workout_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "experiment": "Dynamic Workout Writer (DW²)",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
