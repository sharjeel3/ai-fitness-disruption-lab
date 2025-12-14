"""
Gemini LLM client for AI Fitness Disruption Lab.
Handles all interactions with Google's Gemini API.
"""

import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from .config import config


class GeminiClient:
    """Client for interacting with Gemini LLM."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        config.validate()
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    async def generate_workout(
        self,
        fitness_level: str,
        goals: list[str],
        time_available: int,
        equipment: list[str],
        fatigue: int,
        stress: int,
        sleep_hours: float,
        exercises_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate an adaptive workout based on user inputs.
        
        Args:
            fitness_level: User's fitness level (beginner/intermediate/advanced)
            goals: List of fitness goals (strength/cardio/flexibility)
            time_available: Available workout time in minutes
            equipment: Available equipment list
            fatigue: Fatigue level (1-10)
            stress: Stress level (1-10)
            sleep_hours: Hours of sleep last night
            exercises_data: Optional exercise database
            
        Returns:
            Dictionary containing workout plan and rationale
        """
        
        prompt = f"""You are an expert fitness coach creating a personalized workout.

USER PROFILE:
- Fitness Level: {fitness_level}
- Goals: {', '.join(goals)}
- Time Available: {time_available} minutes
- Equipment: {', '.join(equipment)}
- Current Fatigue: {fatigue}/10
- Current Stress: {stress}/10
- Sleep Last Night: {sleep_hours} hours

INSTRUCTIONS:
1. Design a workout that adapts to their current state (fatigue, stress, sleep)
2. Include 4-6 exercises appropriate for their fitness level
3. Provide sets and reps for each exercise
4. Include a brief rationale explaining why this workout suits their current condition
5. Keep the total duration within {time_available} minutes

SAFETY RULES:
- If fatigue > 7, reduce volume and intensity
- If sleep < 5 hours, focus on mobility/light activity
- If stress > 8, include calming elements
- Never prescribe maximal loads or advanced techniques for beginners

Return your response in this JSON format:
{{
  "workout": [
    {{"exercise": "Exercise Name", "sets": 3, "reps": "8-12", "rest": "60s", "notes": "Form cues"}},
  ],
  "total_duration": {time_available},
  "intensity_level": "moderate",
  "rationale": "Explanation of why this workout suits their current state"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            workout_data = json.loads(response_text.strip())
            return workout_data
            
        except json.JSONDecodeError as e:
            # Fallback response if JSON parsing fails
            return {
                "workout": [
                    {"exercise": "Bodyweight Squat", "sets": 3, "reps": "10-12", "rest": "60s", "notes": "Keep chest up"},
                    {"exercise": "Push-ups", "sets": 3, "reps": "8-10", "rest": "60s", "notes": "Modify on knees if needed"}
                ],
                "total_duration": time_available,
                "intensity_level": "moderate",
                "rationale": f"Adaptive workout generated (parsing error: {str(e)})"
            }
        except Exception as e:
            raise Exception(f"Error generating workout: {str(e)}")
    
    async def generate_text(self, prompt: str) -> str:
        """
        Generate text response from Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text response
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")


# Create singleton instance
gemini_client = GeminiClient()
