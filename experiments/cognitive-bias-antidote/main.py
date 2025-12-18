"""
Cognitive Bias Antidote Engine - Experiment 4
Detects cognitive distortions in fitness thoughts and provides evidence-based reframes.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import google.generativeai as genai
from shared.config import config
from datetime import datetime

app = FastAPI(
    title="Cognitive Bias Antidote Engine",
    description="Detects cognitive distortions in fitness thoughts and provides evidence-based reframes",
    version="1.0.0"
)

# Set up templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Load cognitive bias data
bias_data_path = Path(__file__).parent.parent.parent / "datasets" / "cognitive-biases.json"
with open(bias_data_path, 'r') as f:
    bias_database = json.load(f)


class ThoughtInput(BaseModel):
    """Input schema for cognitive bias detection."""
    
    thought: str = Field(..., description="The user's thought or self-talk statement", min_length=5)
    context: Optional[str] = Field(None, description="Additional context about the situation")
    user_history: Optional[Dict[str, Any]] = Field(None, description="User's workout/progress history")


class BiasDetection(BaseModel):
    """Detected cognitive bias with reframe."""
    
    bias_type: str
    bias_description: str
    confidence: float
    original_thought: str
    detected_patterns: List[str]
    reframe: str
    intervention: str
    intervention_details: Dict[str, Any]
    coaching_tone: str
    actionable_next_step: str
    affirmation: str


class BiasAnalysisResponse(BaseModel):
    """Complete bias analysis response."""
    
    original_thought: str
    context: Optional[str]
    primary_bias: BiasDetection
    secondary_biases: List[BiasDetection]
    overall_assessment: str
    recommended_action: str
    timestamp: str


# Configure Gemini
genai.configure(api_key=config.GEMINI_API_KEY)


def find_matching_biases(thought: str, context: str = None) -> List[Dict[str, Any]]:
    """
    Find cognitive biases that match the thought pattern.
    """
    matching_biases = []
    thought_lower = thought.lower()
    
    for bias in bias_database['biases']:
        # Check if any patterns match the thought
        pattern_matches = [p for p in bias['patterns'] if any(
            keyword in thought_lower for keyword in p.lower().split()[:3]
        )]
        
        if pattern_matches:
            matching_biases.append({
                'bias': bias,
                'matched_patterns': pattern_matches,
                'confidence': len(pattern_matches) / len(bias['patterns'])
            })
    
    # Sort by confidence
    matching_biases.sort(key=lambda x: x['confidence'], reverse=True)
    
    return matching_biases


def generate_bias_analysis(thought: str, context: str = None, user_history: Dict = None) -> BiasAnalysisResponse:
    """
    Use Gemini to perform deep cognitive bias analysis.
    """
    
    # First, get potential matching biases from database
    potential_biases = find_matching_biases(thought, context)
    
    # Prepare context for Gemini
    bias_context = json.dumps(bias_database, indent=2)
    user_context = json.dumps(user_history, indent=2) if user_history else "No history provided"
    
    prompt = f"""You are an expert fitness psychology coach specializing in cognitive behavioral therapy (CBT) for athletes and fitness enthusiasts.

TASK: Analyze the following thought for cognitive biases/distortions that harm fitness progress.

USER'S THOUGHT: "{thought}"
CONTEXT: {context or "No additional context"}
USER HISTORY: {user_context}

AVAILABLE COGNITIVE BIASES DATABASE:
{bias_context}

INSTRUCTIONS:
1. Identify the PRIMARY cognitive bias present in this thought (the most dominant one)
2. Identify any SECONDARY biases (up to 2 additional ones if present)
3. For each bias detected:
   - Explain why this pattern matches the bias
   - Provide a compassionate, evidence-based reframe
   - Suggest a specific intervention from the database
   - Recommend an actionable next step
   - Create a short affirmation statement

4. Provide an overall assessment and recommended action

IMPORTANT:
- Be specific and personalized to the user's actual thought
- Use a warm, non-judgmental tone
- Focus on actionable solutions
- Reference fitness science and psychology where relevant
- If the thought doesn't contain a bias, say so and provide supportive coaching instead

FORMAT YOUR RESPONSE AS JSON:
{{
  "primary_bias": {{
    "type": "bias_type_from_database",
    "description": "brief explanation of the bias",
    "confidence": 0.0-1.0,
    "detected_patterns": ["specific phrases that match"],
    "reframe": "compassionate reframe specific to this thought",
    "intervention": "intervention_type_from_database",
    "intervention_details": {{
      "action": "specific action to take",
      "why": "why this will help"
    }},
    "coaching_tone": "tone_from_database",
    "actionable_next_step": "one specific thing to do right now",
    "affirmation": "short positive affirmation"
  }},
  "secondary_biases": [
    // Same structure as primary_bias, if applicable
  ],
  "overall_assessment": "2-3 sentence summary of the thought pattern",
  "recommended_action": "primary recommendation for moving forward"
}}
"""

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        analysis_data = json.loads(response_text.strip())
        
        # Build BiasDetection objects
        primary_bias = BiasDetection(
            bias_type=analysis_data['primary_bias']['type'],
            bias_description=analysis_data['primary_bias']['description'],
            confidence=analysis_data['primary_bias']['confidence'],
            original_thought=thought,
            detected_patterns=analysis_data['primary_bias']['detected_patterns'],
            reframe=analysis_data['primary_bias']['reframe'],
            intervention=analysis_data['primary_bias']['intervention'],
            intervention_details=analysis_data['primary_bias']['intervention_details'],
            coaching_tone=analysis_data['primary_bias']['coaching_tone'],
            actionable_next_step=analysis_data['primary_bias']['actionable_next_step'],
            affirmation=analysis_data['primary_bias']['affirmation']
        )
        
        secondary_biases = [
            BiasDetection(
                bias_type=bias['type'],
                bias_description=bias['description'],
                confidence=bias['confidence'],
                original_thought=thought,
                detected_patterns=bias['detected_patterns'],
                reframe=bias['reframe'],
                intervention=bias['intervention'],
                intervention_details=bias['intervention_details'],
                coaching_tone=bias['coaching_tone'],
                actionable_next_step=bias['actionable_next_step'],
                affirmation=bias['affirmation']
            )
            for bias in analysis_data.get('secondary_biases', [])
        ]
        
        return BiasAnalysisResponse(
            original_thought=thought,
            context=context,
            primary_bias=primary_bias,
            secondary_biases=secondary_biases,
            overall_assessment=analysis_data['overall_assessment'],
            recommended_action=analysis_data['recommended_action'],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        # Fallback to rule-based matching if Gemini fails
        if potential_biases:
            bias_match = potential_biases[0]
            bias = bias_match['bias']
            
            return BiasAnalysisResponse(
                original_thought=thought,
                context=context,
                primary_bias=BiasDetection(
                    bias_type=bias['type'],
                    bias_description=bias['description'],
                    confidence=bias_match['confidence'],
                    original_thought=thought,
                    detected_patterns=bias_match['matched_patterns'],
                    reframe=bias['reframes'][0],
                    intervention=bias['interventions'][0],
                    intervention_details={
                        "action": f"Try a {bias['interventions'][0]}",
                        "why": "This will help reframe your thinking"
                    },
                    coaching_tone=bias['coaching_tone'],
                    actionable_next_step="Take one small action toward your goal right now",
                    affirmation="You are capable of growth and progress"
                ),
                secondary_biases=[],
                overall_assessment=f"This thought shows signs of {bias['type']} thinking. Remember: progress isn't perfect.",
                recommended_action="Focus on one small action you can take right now",
                timestamp=datetime.now().isoformat()
            )
        else:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with input form."""
    return templates.TemplateResponse("home.html", {
        "request": request,
        "bias_types": [bias['type'] for bias in bias_database['biases']]
    })


@app.post("/analyze", response_model=BiasAnalysisResponse)
async def analyze_thought(input_data: ThoughtInput):
    """
    Analyze a thought for cognitive biases and return reframes.
    """
    analysis = generate_bias_analysis(
        thought=input_data.thought,
        context=input_data.context,
        user_history=input_data.user_history
    )
    
    return analysis


@app.post("/analyze/visual", response_class=HTMLResponse)
async def analyze_thought_visual(
    request: Request, 
    thought: str = Form(...),
    context: Optional[str] = Form(None)
):
    """
    Analyze thought and return visual card output.
    """
    analysis = generate_bias_analysis(
        thought=thought,
        context=context if context else None,
        user_history=None
    )
    
    return templates.TemplateResponse("bias_card.html", {
        "request": request,
        "analysis": analysis
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
