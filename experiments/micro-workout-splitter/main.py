"""
Micro-Workout Splitter Experiment

Breaks long workouts into smaller, achievable time blocks that fit into busy schedules.
Uses Gemini AI to intelligently split workouts based on:
- Available time blocks
- Exercise priorities
- Movement patterns
- Energy distribution
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime
import json

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path for shared modules
sys.path.append(str(Path(__file__).parent.parent.parent))
from shared.config import config

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=config.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Micro-Workout Splitter", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# Load test data
with open("test_data.json", "r") as f:
    test_data = json.load(f)


# --- Pydantic Models ---

class Exercise(BaseModel):
    name: str
    duration: int  # in minutes
    category: str  # mobility, strength, cardio, core
    priority: str = "medium"  # high, medium, low
    sets: Optional[Union[int, str]] = None  # Can be number or "AMRAP", "Timed", etc.
    reps: Optional[str] = None
    rest: Optional[Union[int, str]] = None  # Can be seconds or "as needed"
    duration_per_set: Optional[str] = None
    color: Optional[str] = None  # For UI visualization


class Workout(BaseModel):
    name: str
    total_duration: int
    exercises: List[Exercise]


class SplitRequest(BaseModel):
    workout: Workout
    available_blocks: List[int] = Field(..., description="Available time blocks in minutes")
    scenario: Optional[str] = Field(None, description="Context like 'busy parent' or 'office worker'")


class WorkoutSegment(BaseModel):
    block_number: int
    duration: int
    focus: str
    exercises: List[Exercise]
    completion_time: str  # e.g., "Morning", "Lunch break", "Evening"
    rationale: str


class SplitResponse(BaseModel):
    original_workout: str
    total_time: int
    segments: List[WorkoutSegment]
    coverage_percentage: float
    ai_insights: str


# --- Helper Functions ---

def build_split_prompt(workout: Workout, time_blocks: List[int], scenario: Optional[str]) -> str:
    """Build the prompt for Gemini to split the workout intelligently."""
    
    exercises_text = "\n".join([
        f"- {ex.name}: {ex.duration} min, Category: {ex.category}, Priority: {ex.priority}"
        for ex in workout.exercises
    ])
    
    scenario_context = f"Context: {scenario}\n" if scenario else ""
    
    prompt = f"""You are an expert fitness coach helping someone with a fragmented schedule.

{scenario_context}
**Full Workout to Split:**
Name: {workout.name}
Total Duration: {workout.total_duration} minutes

**Exercises:**
{exercises_text}

**Available Time Blocks:** {', '.join([f'{b} min' for b in time_blocks])}

**Your Task:**
Intelligently split this workout into the available time blocks following these rules:

1. **Prioritize high-priority exercises** - include them first
2. **Group by movement patterns** - don't split similar exercises awkwardly
3. **Maintain workout logic** - warm-up first, cool-down last when possible
4. **Balance intensity** - don't cram all hard exercises in one block
5. **Maximize coverage** - use as much of the available time as possible
6. **Suggest timing** - indicate best time of day for each segment (e.g., "Morning - 7am", "Lunch break", "Evening")

Return a JSON response with this structure:
{{
  "segments": [
    {{
      "block_number": 1,
      "duration": <actual minutes used>,
      "focus": "<primary focus like 'Lower body strength' or 'Mobility + Core'>",
      "exercises": [
        {{
          "name": "<exercise name>",
          "duration": <minutes>,
          "category": "<category>",
          "priority": "<priority>",
          "sets": <if applicable>,
          "reps": "<if applicable>"
        }}
      ],
      "completion_time": "<suggested time like 'Morning - 7am' or 'Lunch break'>",
      "rationale": "<brief explanation of why these exercises go together>"
    }}
  ],
  "coverage_percentage": <percentage of original workout covered>,
  "ai_insights": "<2-3 sentence summary of the split strategy and any trade-offs made>"
}}

Provide ONLY valid JSON, no additional text."""
    
    return prompt


async def split_workout_with_ai(workout: Workout, time_blocks: List[int], scenario: Optional[str]) -> SplitResponse:
    """Use Gemini to intelligently split the workout."""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = build_split_prompt(workout, time_blocks, scenario)
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean up markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()
        
        # Parse JSON response
        result = json.loads(result_text)
        
        # Convert to SplitResponse
        segments = [
            WorkoutSegment(
                block_number=seg["block_number"],
                duration=seg["duration"],
                focus=seg["focus"],
                exercises=[Exercise(**ex) for ex in seg["exercises"]],
                completion_time=seg["completion_time"],
                rationale=seg["rationale"]
            )
            for seg in result["segments"]
        ]
        
        return SplitResponse(
            original_workout=workout.name,
            total_time=sum(block.duration for block in segments),
            segments=segments,
            coverage_percentage=result["coverage_percentage"],
            ai_insights=result["ai_insights"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")


def get_category_color(category: str) -> str:
    """Return color code for workout categories."""
    colors = {
        "mobility": "#a8edea",
        "strength": "#667eea",
        "cardio": "#fa709a",
        "core": "#43e97b"
    }
    return colors.get(category.lower(), "#cccccc")


# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with input form."""
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "test_workouts": test_data["sample_workouts"],
            "test_scenarios": test_data["sample_time_blocks"]
        }
    )


@app.post("/split", response_class=HTMLResponse)
async def split_workout_form(
    request: Request,
    workout: int = Form(...),
    scenario: str = Form(""),
    block1: int = Form(None),
    block2: int = Form(None),
    block3: int = Form(None),
    block4: int = Form(None)
):
    """Form submission endpoint to split a workout into micro-segments."""
    
    # Get workout from test data
    if workout < 0 or workout >= len(test_data["sample_workouts"]):
        raise HTTPException(status_code=400, detail="Invalid workout selection")
    
    workout_data = Workout(**test_data["sample_workouts"][workout])
    
    # Collect time blocks
    available_blocks = [b for b in [block1, block2, block3, block4] if b is not None and b > 0]
    
    if not available_blocks:
        raise HTTPException(status_code=400, detail="Must provide at least one time block")
    
    # Create split request
    split_request = SplitRequest(
        workout=workout_data,
        available_blocks=available_blocks,
        scenario=scenario if scenario else None
    )
    
    # Call AI to split workout
    result = await split_workout_with_ai(
        split_request.workout,
        split_request.available_blocks,
        split_request.scenario
    )
    
    # Add color coding for visualization
    for segment in result.segments:
        for exercise in segment.exercises:
            exercise.color = get_category_color(exercise.category)
    
    # Save output
    output_data = result.dict()
    output_data["timestamp"] = datetime.now().isoformat()
    
    output_file = f"outputs/split_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    return templates.TemplateResponse(
        "workout_splitter.html",
        {
            "request": request,
            "result": result,
            "scenario": split_request.scenario or "Custom schedule"
        }
    )


@app.post("/api/split")
async def split_workout_api(split_request: SplitRequest):
    """JSON API endpoint to split a workout into micro-segments."""
    
    # Validate time blocks
    if not split_request.available_blocks:
        raise HTTPException(status_code=400, detail="Must provide at least one time block")
    
    # Call AI to split workout
    result = await split_workout_with_ai(
        split_request.workout,
        split_request.available_blocks,
        split_request.scenario
    )
    
    return result


@app.get("/demo", response_class=HTMLResponse)
async def demo(request: Request):
    """Demo with pre-loaded data."""
    
    # Use first test workout and scenario
    workout_data = Workout(**test_data["sample_workouts"][0])
    time_blocks = test_data["sample_time_blocks"][0]["available_blocks"]
    scenario = test_data["sample_time_blocks"][0]["scenario"]
    
    split_request = SplitRequest(
        workout=workout_data,
        available_blocks=time_blocks,
        scenario=scenario
    )
    
    # Call AI to split workout
    result = await split_workout_with_ai(
        split_request.workout,
        split_request.available_blocks,
        split_request.scenario
    )
    
    # Add color coding for visualization
    for segment in result.segments:
        for exercise in segment.exercises:
            exercise.color = get_category_color(exercise.category)
    
    # Save output
    output_data = result.dict()
    output_data["timestamp"] = datetime.now().isoformat()
    
    output_file = f"outputs/split_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    return templates.TemplateResponse(
        "workout_splitter.html",
        {
            "request": request,
            "result": result,
            "scenario": scenario
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "micro-workout-splitter"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
