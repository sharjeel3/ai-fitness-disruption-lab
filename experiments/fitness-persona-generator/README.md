# 🎭 Fitness Persona Generator

**Generate unique, AI-powered fitness identity cards based on personality traits, goals, and preferences.**

## Overview

The Fitness Persona Generator uses Gemini LLM to create personalized fitness identities that go beyond generic profiles. It analyzes user traits, goals, and preferences to generate inspiring personas with custom names, taglines, color schemes, and motivational messaging.

## What It Does

- **Analyzes** user personality traits and fitness goals
- **Matches** users to existing archetypes or creates unique hybrid personas
- **Generates** creative persona names (e.g., "The Precision Phoenix")
- **Creates** memorable 3-word taglines (e.g., "Rise. Refine. Repeat.")
- **Designs** personalized color palettes that match the persona's energy
- **Provides** motivational quotes and training recommendations

## Why It's Disruptive

Current fitness apps treat users as data points with generic profiles. This prototype demonstrates:

1. **Identity-Driven Fitness**: Users aren't just "beginner" or "advanced" - they're unique personas with distinct training philosophies
2. **Emotional Connection**: Custom names, taglines, and quotes create deeper engagement
3. **Shareability**: Beautiful persona cards are designed to be screenshot and shared
4. **Personalization at Scale**: AI generates infinite unique personas while maintaining quality

## Technology Stack

- **Backend**: FastAPI
- **LLM**: Google Gemini 2.5 Flash Lite
- **Templates**: Jinja2
- **Styling**: Pure CSS (iOS-inspired mobile-first design)

## Installation

### Prerequisites

- Python 3.10+
- Google AI Studio API key

### Setup

```bash
# Navigate to experiment directory
cd experiments/fitness-persona-generator

# Ensure virtual environment is activated
source ../../../venv/bin/activate  # macOS/Linux
# or
..\..\..\venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (if not already done at project root)
# Create .env file with GEMINI_API_KEY
```

## Running the Prototype

```bash
# Ensure virtual environment is activated
source ../../../venv/bin/activate  # macOS/Linux

# Start the server
uvicorn main:app --reload --port 8006

# Access the application
# Home page: http://localhost:8006
# API docs: http://localhost:8006/docs
# Demo: http://localhost:8006/demo
```

## API Endpoints

### `GET /`
Home page with interactive persona creation form.

### `POST /generate`
Generate a persona based on user input.

**Request Body:**
```json
{
  "traits": ["disciplined", "creative", "consistent"],
  "goals": ["strength", "lean"],
  "music_preference": "instrumental",
  "workout_style": "controlled intensity",
  "session_length_preference": 45
}
```

**Response:**
HTML persona card (screenshot-ready)

### `GET /demo`
Pre-filled demo persona for testing.

### `GET /api/archetypes`
Get all available persona archetypes from the dataset.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `traits` | array[string] | Yes | 1-5 personality traits (e.g., disciplined, creative) |
| `goals` | array[string] | Yes | 1-3 fitness goals (e.g., strength, lean) |
| `music_preference` | string | Yes | Workout music genre |
| `workout_style` | string | No | Preferred style (e.g., intense, gentle) |
| `session_length_preference` | integer | No | Ideal session length (10-120 minutes) |

## Output Structure

```json
{
  "persona_name": "The Precision Phoenix",
  "archetype_match": "The Precision Phoenix",
  "style": "controlled intensity",
  "tagline": "Rise. Refine. Repeat.",
  "traits": ["disciplined", "creative", "consistent"],
  "goals": ["strength", "lean"],
  "color_palette": ["#FF6B35", "#FFD23F"],
  "music_preference": "instrumental",
  "workout_approach": "structured_progressive",
  "ideal_session_length": 45,
  "recovery_priority": "medium",
  "description": "You are a master of precision...",
  "motivation_quote": "Excellence is not an act, but a habit..."
}
```

## Visual Output

The persona card features:

- **Header**: Gradient background with persona colors, icon, name, and tagline
- **Identity Section**: AI-generated description of the persona
- **Motivation**: Inspirational quote in a styled quote box
- **Traits & Goals**: Tagged display of user attributes
- **Training Profile**: Session length and recovery priority stats
- **Details**: Workout style, approach, and music preference

### Design Features

- 375px width (iPhone-optimized)
- Custom gradient colors per persona
- Clean, modern iOS-inspired styling
- Screenshot-ready format
- Print-friendly (save to PDF)

## Example Use Cases

### 1. Onboarding Flow
New users discover their fitness identity during app onboarding, creating immediate engagement.

### 2. Social Sharing
Users share their persona cards on social media, driving organic growth.

### 3. Community Building
Group users by persona types for challenges and community features.

### 4. Training Personalization
Use persona attributes to customize workout recommendations and coaching tone.

## Testing

### Manual Testing

1. **Quick Test (Demo)**:
   ```bash
   # Visit http://localhost:8006/demo
   # Should display a pre-generated persona
   ```

2. **Custom Input**:
   - Navigate to http://localhost:8006
   - Add 2-3 traits (e.g., disciplined, creative)
   - Add 1-2 goals (e.g., strength, lean)
   - Select music preference
   - Click "Generate My Persona"

3. **Screenshot Test**:
   - Generate a persona
   - Use browser DevTools (Device Emulation → iPhone 14)
   - Take screenshot (Cmd+Shift+4 on macOS)

### API Testing

```bash
# Test with curl
curl -X POST http://localhost:8006/generate \
  -H "Content-Type: application/json" \
  -d '{
    "traits": ["disciplined", "analytical"],
    "goals": ["strength"],
    "music_preference": "rock"
  }'
```

## Dataset

Uses `/datasets/personas.json` which contains:
- Pre-defined archetype templates
- Trait-goal mappings
- Color palette suggestions
- Training style definitions

## Limitations & Safety

### Current Limitations
- Persona generation requires API call (not offline)
- Limited to English language
- No user account/persistence

### Safety Boundaries
- No medical or diagnostic claims
- Maintains positive, empowering tone
- Avoids extreme or unhealthy fitness goals
- All personas promote sustainable fitness approaches

## Future Enhancements

1. **Persona Evolution**: Track how personas change over time as users progress
2. **Community Matching**: Connect users with similar personas
3. **Workout Templates**: Auto-generate workouts based on persona attributes
4. **Avatar Generation**: Use image AI to create visual persona avatars
5. **Multi-language Support**: Generate personas in multiple languages

## Troubleshooting

### Common Issues

**"Failed to parse AI response"**
- Check your Gemini API key is valid
- Verify API quota hasn't been exceeded
- Check network connection

**"Please add at least one trait/goal"**
- Ensure traits/goals are added before submitting
- Click example tags or type and press Enter

**Styling looks broken**
- Clear browser cache
- Check browser DevTools for console errors
- Verify templates are properly loaded

## Port Configuration

Default port: **8006**

To change:
```bash
uvicorn main:app --reload --port YOUR_PORT
```

## Screenshots

Save generated personas to:
```
/outputs/latest_persona.json  # JSON output
```

Take screenshots from browser and save to:
```
/outputs/persona_screenshots/
```

## Contributing

This is a prototype experiment. To improve:

1. Test with various trait/goal combinations
2. Evaluate persona quality and creativity
3. Suggest new archetype templates
4. Report bugs or edge cases

## License

Part of AI Fitness Disruption Lab. See project root LICENSE file.
